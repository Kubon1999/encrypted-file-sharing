import PySimpleGUI as sg

sg.theme('DarkAmber')

layout = [[sg.Text('Row 1 text hahahaha')],
          [sg.Text('Row 2 text hahahaha'), sg.InputText()],
          [sg.Button('Ok'), sg.Button('Cancel')]]

layout2 = [[sg.Text('Row 1 text hahahaha'), sg.InputText()],
          [sg.Text('Row 2 text hahahaha')],
          [sg.Button('Ok'), sg.Button('Cancel')]]

window = sg.Window('Window title', layout)

while True:
    event, values = window.read();
    if event == sg.WIN_CLOSED or event == 'Cancel':
        break

    print('You entered ',values[0])
window.close()