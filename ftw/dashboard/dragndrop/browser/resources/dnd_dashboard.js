jQuery(function($){

  var updateDropZoneHeight = function() {
    $('.dashboard-column').css('min-height', '0px');
    var sizes = [];
    $('.dashboard-column').each(function(index, value){
      sizes.push($(value).height());
    });
    // set biggest value in array as min-height
    $('.dashboard-column').css('min-height', Math.max.apply(Math, sizes)+'px');
  };

  updateDropZoneHeight();

  var print_images = function(obj){
    // Fold functionality always
    if($('.documentEditable').length !== 0){
      var actions = '<div class="portletActionsWrapper">';
      if (obj.parents('.portletwrapper:first').hasClass('folded')) {
        actions += "<a class='dashboardButton buttonOpen' href='#'>&nbsp;</a>";
      }
      else{
        actions+="<a class='dashboardButton buttonClose' href='#'>&nbsp;</a>";
      }
      //Hash auslessen
      var hash = obj.parents('.portletwrapper:first').attr('id').substr('portletwrapper-'.length);
      actions += '<span class="dashboardButton buttonMove">&nbsp;</span>';
      if (obj.parents('.portletwrapper:first').hasClass('editable')) {
        actions += '<a class="dashboardButton buttonEdit" href="dashboardEditLinkView?hash='+hash+'">&nbsp;</a>';
      }
      actions += '<a class="dashboardButton buttonRemove" href="#">&nbsp;</a>';
      actions += '</div>';
      $(actions).insertAfter($('.portletTopLeft',obj));
    }
  };

  var authenticator_token = $('.dashboardContent').data('authenticator-token');

  var update_dashboard_order = function(event, ui) {
    // the update event handler is called twice (once with ui.sender
    // and once without). ui.sender needs to be Null, otherwise
    // dragging within one column doesnt work
    if(ui.sender) {
      return;
    }
    var customSerialization = function() {
      // prepare data
      var portlets = $('.portletwrapper');
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
          if($('#portletwrapper-'+ oldHash).hasClass('kssattr-portlethash-'+oldHash)){
            var classes = $('#portletwrapper-' + oldHash).attr('class');
            if(classes!==null) {
              classes = classes.replace('kssattr-portlethash-' + oldHash, 'kssattr-portlethash-'+ newHash);
              $('#portletwrapper-'+ oldHash).attr('class', classes);
            }
          }

          $('#portletwrapper-' + oldHash).attr('id', 'portletwrapper-' + newHash);

          // edit link must be fixed: the column id may be wrong!
          // test if there is a edit link
          var editLinks = $('#portletwrapper-' + newHash + ' .buttonEdit');
          if(editLinks.length>0) {
            var editLink = editLinks[0];
            var href = editLink.getAttribute("href").replace(oldHash, newHash);
            editLink.setAttribute('href', href);
          }
        }
      }
    };
    // send changes to server and update hashes
    $.ajax({
      type :      'POST',
      url :       './ftw.dashboard.dragndrop-update_order',
      data :      customSerialization(),
      beforeSend: function (request){
        request.setRequestHeader("X-CSRF-TOKEN", authenticator_token);
      },
      success :   function(msg) {
        updateHashesCallback(msg);
        // we need to send the changes with updated hashes again
        $.ajax({
          type :      'POST',
          url :       './ftw.dashboard.dragndrop-update_order',
          beforeSend: function (request){
            request.setRequestHeader("X-CSRF-TOKEN", authenticator_token);
          },
          data :      customSerialization()
        });
      }
    });
  };

  $('.dashboard-column').sortable({
    connectWith :   $('.dashboard-column'),
    cursor :        'move',
    start :         function(){$('body').addClass('dragPortlet');},
    stop :          function(){$('body').removeClass('dragPortlet');updateDropZoneHeight();},
    distance :      10,
    handle :        '.portletHeader',
    revert :        true,
    tolerance :     'pointer',
    update :        update_dashboard_order
  });

  /* TOGGLE PORTLET CONTENT */
  $('.portletHeader a.buttonOpen, .portletHeader a.buttonClose').live('click',function(e) {
    e.preventDefault();
    $(this).parents('.portletwrapper:first').toggleClass('folded');
    //Change icon
    $(this).toggleClass('buttonClose').toggleClass('buttonOpen');

    var wrapper = $(this).parents('.portletwrapper:first');
    var hash = wrapper.attr('id').substr('portletwrapper-'.length);

    var folded = 0;
    if ($(this).parents('.portletwrapper:first').hasClass('folded')) {
      folded = 1;
    }
    $.ajax({
      type :      'POST',
      beforeSend: function (request){
        request.setRequestHeader("X-CSRF-TOKEN", authenticator_token);
      },
      url :       './ftw.dashboard.dragndrop-foldportlet',
      data :      'hash='.concat(hash)+'&folded='.concat(folded)
    });

    //special workarround for fav portlet
    if ($(this).parents('.portletwrapper:first').find('.portletItem').length===0){
      $(this).parents('.portletwrapper:first').find('.portletItemEmpty').toggle().end();
    }
  });

  // This is needed when the calendar reloads to display the next month
  $('.portletwrapper .portletHeader a').live('click', function(){
    $(this).append($('<div class="resetIcons"></div>'));
    var wrapper = $(this).parents('.portletwrapper:first');
    var column = wrapper.parents('.dashboard-column:first');
    var wrapper_id = wrapper.attr('id');
    var reset_icon = function(){
      var obj = $(column).find('#'+wrapper_id);
      if ($('.resetIcons', obj).length>0){
        setTimeout((reset_icon), 100);
      } else {
        print_images($('.portletHeader', obj));
      }
    };
    reset_icon();
  });

  /* REMOVE PORTLET */
  $('.portletHeader a.buttonRemove').live('click',function(e) {
    e.preventDefault();
    var wrapper = $(this).parents('.portletwrapper:first');
    var hash = wrapper.attr('id').substr('portletwrapper-'.length);
    $('<div></div>').
      html('<div id="remove-portlet-dialog">'+$('#text-remove-portlet').html()+'</div>').
      dialog({
        modal: true, resizable: false, position: {my: "center", at: "top+200"}, width: 1200,
        buttons: [
          {
            text: $("#text-remove-portlet-yes").html(),
            click: function () {
              $.ajax({
                type : 'POST',
                url : './ftw.dashboard.dragndrop-removeportlet',
                beforeSend: function (request){
                  request.setRequestHeader("X-CSRF-TOKEN", authenticator_token);
                },
                data : 'hash='.concat(hash)
              });
              // destroy it
              wrapper.hide().remove();
              $(this).dialog("close");
            }
          },
          {
            text: $("#text-remove-portlet-no").html(),
            click: function () {
              $(this).dialog("close");
            }
          }
        ],
        close: function (event, ui) {
          $(this).remove();
        }
      });
  });

  /* REMOVE Favourite*/
  $('.portletFavourites .close.favRemove').live('click',function(e){
    var uid = $(this).attr('id');
    $.post('./ftw_dashboard_dragndrop_remove_favorite',{ uid : uid },function(data){
      if (data===''){
        alert('for some reason the favorite could not be delted, sorry');
      }
      if (data=='OK'){

        $('[id='+uid+']').closest('.portletItem').each(function(i,v){
          $(v).remove();
        });

        if ($('.portletFavourites .close.favRemove').length===0){
          $('span.noFavs').closest('.portletItemEmpty').show();
        }
      }

    });
  });

  $('.dashboard-column .portletHeader').each(function(){
    print_images($(this));
  });


});
