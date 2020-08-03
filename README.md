A simple package to create your own GUI.

To get started and create your own GUI, simply write:

    from customGUI.form_creator import FormCreator
    
    fc = FormCreator('save.txt')

    fc.run()

To add a new icon select the name of the icon from the taskbar on the left. Once selected,
the item will appear on the Form (unless the chosen item is a Form). Then any of the icon
settings can be modified, including appearance and behaviour. To modify a setting, a correct
value must be input. In case a value is incorrect, a message will appear at the bottom with 
instructions on how to input a correct value. Always press Enter to save a new value, otherwise
it won't be remembered.

Each icon must have a unique name, which will be used when using the form later in your 
application.

To save the Form to be able to use it later, press CTRL+S. It will be saved to the file path
specified when creating an object of the FormCreator class (eg.: 'save.txt').

In order to load the form from the save file and use it as a standalone window, the following 
needs to be written:

    from customGUI.form_loader import FormLoader
    
    fl = FormLoader('save.txt')
    
    fl.load()
    
    while True:
        fl.update()
        
You can access items from the Form by calling fl.objects['_name of an item_']. This will return
the corresponding item (or rather an object of the same class with all parameters copied). You can
then modify all parameters as you wish. For example if the object is of the Textbox class, you
can change the _text_ parameter, by calling fl.objects['_name of the Textbox_'].text.

Other possibilities of this library shall be explained in the non-existent-so-far Documentation.
      
