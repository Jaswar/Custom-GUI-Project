A simple package to create your own GUI.

To get started and create your own GUI, simply write:

    from customGUI.form_creator import FormCreator
    
    fc = FormCreator('save.txt')

    while True:
        fc.update()

Once you click CTRL+S, your newly created form will be saved to 'save.txt'.