Overview
========


`ftw.dashboard.dragndrop` adds persistent dragndrop functionality to the standard plone dashboard.

.. figure:: http://onegov.ch/approved.png/image
   :align: right
   :target: http://onegov.ch/community/zertifizierte-module/ftw.dashboard.dragndrop

   Certified: 01/2013

Features:

- **Drag'n'drop**:
  All dashboard portlets can be moved with drag'n'drop from column to column and reordered in the column.
- **Folding**:
  Dashboard porlets are foldable.
- **Edit portlet icon**:
  Dashboard portlets have an icon on the top (pencil) for editing the portlet.
- **close/remove portlet**:
  Dashboard portlets have an icon on the top (cross) for removing the portlet from the dashboard.
- **dashboard macro**:
  The Dashboard is a dedicated view, but it can also be included in other pages as follows if
  its BrowserView extends `FTWDashBoard`:

::

    <div tal:attributes="id string:regio-content;
                       class python:view.editable and 'documentEditable' or ''" >

      <div metal:use-macro="context/@@dashboard/macros/dashboard">
          dashboard from ftw.dashboard.dragndrop product
      </div>
    </div>


Install
=======

- Add ``ftw.dashboard.dragndrop`` to your buildout configuration:

::

  [instance]
  eggs =
    ftw.dashboard.dragndrop

- Run buildout.

- Install ``ftw.dashboard.dragndrop`` in portal_setup.

- Configure the dashboard in the ``portal_properties`` tool (addablePortlets).


Properties:
===========

- **dashboardEditable**:
  True: The dashboard will always be editable, all functionalities are available
  False: The standard view (``@@dashboard``) will only provide the dragndrop and the fold functionality. Use the ``@@manage-dashbord`` view to customize your dashboard.

- **columnNumber**:
  Number of dashboard columns. There are only 4 portlet managers provided by plone. If you need more you need to register additional dashboard portlet managers.

- **addablePortlets**:
  Defines the addable portlets.
  You can use "portlet.Calendar" or "portlet.Calendar:Portlet Calendar". With the latter form you can change the title of the portlet.
  You ca also use "@@my-view:My custom view, which adds a portlet". If the first parts starts with "@@", the given view will be called.

- **showleftcolumn**:
  Displays the plone.leftcolumn

- **showrightcolumn**:
  Displays the plone.rightcolumn


Links
=====

- Github: https://github.com/4teamwork/ftw.dashboard.dragndrop
- Issues: https://github.com/4teamwork/ftw.dashboard.dragndrop/issues
- Pypi: http://pypi.python.org/pypi/ftw.dashboard.dragndrop
- Continuous integration: https://jenkins.4teamwork.ch/search?q=ftw.dashboard.dragndrop


Copyright
---------

This package is copyright by `4teamwork <http://www.4teamwork.ch/>`_.

``ftw.dashboard.dragndrop`` is licensed under GNU General Public License, version 2.
