jq(function() {

    var updateDropZoneHeight = function() {
      jq('.dashboard-column').css('min-height', '0px');
      var sizes = []
      jq('.dashboard-column').each(function(index, value){
        sizes.push(jq(value).height());
      });
      // set biggest value in array as min-height
      jq('.dashboard-column').css('min-height', Math.max.apply(Math, sizes)+'px');
    };

    updateDropZoneHeight();

    var print_images = function(obj){
        var actions = '<div class="portletActionsWrapper">';
        // Fold functionality always
        if(jq('.documentEditable').length !== 0){
            if (obj.parents('.portletwrapper:first').hasClass('folded')) {
                actions += "<a class='dashboardButton buttonOpen' href='#'>&nbsp;</a>";
            }
            else{
                actions+="<a class='dashboardButton buttonClose' href='#'>&nbsp;</a>";
            }
            //Hash auslessen
            var hash = obj.parents('.portletwrapper:first')[0].id.substr('portletwrapper-'.length);
            actions += '<span class="dashboardButton buttonMove">&nbsp;</span>';
            if (obj.parents('.portletwrapper:first').hasClass('editable')) {
                actions += '<a class="dashboardButton buttonEdit" href="dashboardEditLinkView?hash='+hash+'">&nbsp;</a>';
            }
            actions += '<a class="dashboardButton buttonRemove" href="#">&nbsp;</a>';
        }
        actions += '</div>';
        jq(actions).insertAfter(jq('.portletTopLeft',obj));
    };

    var update_dashboard_order = function(event, ui) {
        // the update event handler is called twice (once with ui.sender
        // and once without). ui.sender needs to be Null, otherwise
        // dragging within one column doesnt work
        if(ui.sender) {
            return;
        }
        var customSerialization = function() {
            // prepare data
            var portlets = jq('.portletwrapper');
            var data = new Array();
            for(var i=0; i<portlets.length; i++) {
                var portlet = portlets[i];
                var column_id = portlet.parentNode.id.replace('dashboard-portlets', 'plone.dashboard');
                var hash = portlet.id.substr('portletwrapper-'.length);
                data.push('portlets:list=' + column_id + ':' + hash);
            }
            return data.join('&');
        };
        var updateHashesCallback = function(msg) {
            // parse response
            if(msg.length>0) {
                var data = msg.split(';');
                for(var i=0; i<data.length; i++) {
                    // moved portlets have new hashes
                    var replace = data[i].split(':');
                    var oldHash = replace[0];
                    var newHash = replace[1];

                    //kss attribute portlethash must be fixed
                    if(jq('#portletwrapper-'+ oldHash).hasClass('kssattr-portlethash-'+oldHash)){
                        var classes = jq('#portletwrapper-' + oldHash)[0].getAttribute('class');
                        if(classes!==null) {
                            classes = classes.replace('kssattr-portlethash-' + oldHash, 'kssattr-portlethash-'+ newHash);
                            jq('#portletwrapper-'+ oldHash)[0].setAttribute('class', classes);
                        }
                    }

                    jq('#portletwrapper-' + oldHash)[0].setAttribute('id', 'portletwrapper-' + newHash);

                    // edit link must be fixed: the column id may be wrong!
                    // test if there is a edit link
                    var editLinks = jq('#portletwrapper-' + newHash + ' .edit');
                    if(editLinks.length>0) {
                        var editLink = editLinks[0];
                        var href = editLink.getAttribute("href").replace(oldHash, newHash);
                        editLink.setAttribute('href', href);
                    }
                }
            }
        };
        // send changes to server and update hashes
        jq.ajax({
            type :      'POST',
            url :       './ftw.dashboard.dragndrop-update_order',
            data :      customSerialization(),
            success :   function(msg) {
                updateHashesCallback(msg);
                // we need to send the changes with updated hashes again
                jq.ajax({
                    type :      'POST',
                    url :       './ftw.dashboard.dragndrop-update_order',
                    data :      customSerialization()
                });
            }
        });
    };

    jq('.dashboard-column').sortable({
        connectWith :   jq('.dashboard-column'),
        cursor :        'move',
        start :         function(){jq('body').addClass('dragPortlet');},
        stop :          function(){jq('body').removeClass('dragPortlet');updateDropZoneHeight();},
        distance :      10,
        handle :        '.portletHeader',
        revert :        true,
        tolerance :     'pointer',
        update :        update_dashboard_order
    });

    jq('.column').disableSelection();

    /* TOGGLE PORTLET CONTENT */
    jq('.portletHeader a.buttonOpen, .portletHeader a.buttonClose').live('click',function(e) {
      e.preventDefault();
        jq(this).parents('.portletwrapper:first').toggleClass('folded');
        //Change icon
        jq(this).toggleClass('buttonClose').toggleClass('buttonOpen');

        var wrapper = jq(this).parents('.portletwrapper:first');
        var hash = wrapper[0].id.substr('portletwrapper-'.length);

        var folded = 0;
        if (jq(this).parents('.portletwrapper:first').hasClass('folded')) {
            folded = 1;
        }
        jq.ajax({
            type :      'POST',
            url :       './ftw.dashboard.dragndrop-foldportlet',
            data :      'hash='.concat(hash)+'&folded='.concat(folded)
        });

        //special workarround for fav portlet
        if (jq(this).parents('.portletwrapper:first').find('.portletItem').length===0){
            jq(this).parents('.portletwrapper:first').find('.portletItemEmpty').toggle().end();
            }
    });

    /* REMOVE PORTLET */
    jq('.portletHeader a.buttonRemove').live('click',function(e) {
        e.preventDefault();
        var wrapper = jq(this).parents('.portletwrapper:first');
        var hash = wrapper[0].id.substr('portletwrapper-'.length);
        // request
        jq.ajax({
            type :      'POST',
            url :       './ftw.dashboard.dragndrop-removeportlet',
            data :      'hash='.concat(hash)
        });
        // destroy it
        wrapper.hide().remove();
    });

    // This is needed when the calendar reloads to display the next month
    jq('.portletwrapper .portletHeader a').live('click', function(){
        jq(this).append(jq('<div class="crap"></div>'));
        var wrapper = jq(this).parents('.portletwrapper:first');
        var column = wrapper.parents('.dashboard-column:first');
        var wrapper_id = wrapper.attr('id');
        var reset_icon = function(){
            var obj = jq(column).find('#'+wrapper_id);
            if (jq('.crap', obj).length>0){
                setTimeout((reset_icon), 100);
            } else {
                print_images(jq( '.portletHeader',obj));
            }
        };
        reset_icon();
    });

    /* REMOVE Favourite*/
    jq('.portletFavourites .close.favRemove').live('click',function(e){
        var uid = jq(this).attr('id');
        jq.post('./ftw_dashboard_dragndrop_remove_favorite',{ uid : uid },function(data){
            if (data===''){
                alert('for some reason the favorite could not be delted, sorry');
            }
            if (data=='OK'){

                jq('[id='+uid+']').closest('.portletItem').each(function(i,v){
                    jq(v).remove();
                });

                if (jq('.portletFavourites .close.favRemove').length===0){
                    jq('span.noFavs').closest('.portletItemEmpty').show();
                }
            }

        });
    });

    jq('.dashboard-column .portletHeader').each(function(){
        print_images(jq(this));
    });


});
