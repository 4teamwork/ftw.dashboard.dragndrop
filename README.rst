Overview
========


`ftw.dashboard.dragndrop` adds persistent dragndrop functionality to the standard plone dashboard.

Features:

- **Drag'n'drop**:
  All dashboard portlets can be moved with drag'n'drop from column to column and reordered in the column.
- **Folding**:
  Dashboard porlets are foldable.
- **Edit portlet icon**:
  Dashboard portlets have an icon on the top (pencil) for editing the portlet.
- **close/remove portlet**:
  Dashboard portlets have an icon on the top (cross) for removing the portlet from the dashboard.


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
-----------

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

- Package repository: https://github.com/4teamwork/ftw.dashboard.dragndrop
- Issue tracker: https://github.com/4teamwork/ftw.dashboard.dragndrop/issues
- Package on pypi: http://pypi.python.org/pypi/ftw.dashboard.dragndrop
- Continuous integration: https://jenkins.4teamwork.ch/search/?q=ftw.dashboard.dragndrop

Maintainer
==========

This package is produced and maintained by `4teamwork GmbH <http://www.4teamwork.ch/>`_.