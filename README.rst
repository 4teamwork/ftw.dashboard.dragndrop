Overview
========


The ftw.dashboard.dragndrop - packet add persistent dragndrop functionality to standard plone dashboard.
Additional it add icons for fold, edit and close/remove functionality

Features:
- persistent dragndrop
    all portlets can moved with dragndrop functionality from column to column and also in the column
- persistent fold:
    all portlets have an icon on the top (triangle) wich provide the persistent fold function
- edit portlet 
    all portlets have an icon on the top (pensil) wich links to the respective Edit Page.
- close/remove portlet
    all portlets have an icon on the top (cross) wich remove the respective portlet from the dashboard


Install
======

- Add ``ftw.ftw.dashboard.dragndrop`` to your buildout configuration

:: 
  [instance]
  eggs = 
    ftw.blog
    
- Run buildout

- Install ``ftw.blog`` in portal_setup

- Customize the properties (addablePortlets)


Properties:
-----------

dashboardEditable: 
True: The dashboard will always show up the edit-mode, all functionalities are available 
False: The standard view (/dashboard) will only show the dragndrop and the fold functionality. Use manage-dashbord view to customize your dashboard.  

columnNumber: 
Number of Dashboard-Columns. 
(if more than 4 columns, you have to add new PortletMangers)

addablePortlets: 
Defines the addable portlets.
You can use "portlet.Calendar" or "portlet.Calendar:Portlet Calendar", after colon is a user friendly name - added in release 1.1


Links
=====

- Package repository: https://github.com/4teamwork/ftw.dashboard.dragndrop
- Issue tracker: https://github.com/4teamwork/ftw.dashboard.dragndrop/issues
- Package on pypi: http://pypi.python.org/pypi/ftw.dashboard.dragndrop
- Continous integration: https://jenkins.4teamwork.ch/job/ftw.dashboard.dragndrop/

Maintainer
==========

This package is produced and maintained by `4teamwork GmbH <http://www.4teamwork.ch/>`_.
