import PySimpleGUI as sg      

sg.theme('DarkBlue2')    # Keep things interesting for your users

loadinglayout = [[sg.Text('Please wait while the Waffle Chef loads.')]]

layout = [[sg.Text('AI Waffle Chef')],        
        [sg.Text('Creativity:'), sg.Text('', key='_OUTPUT_')],  
        [sg.Slider((1,100), key='_SLIDER_', orientation='h', enable_events=True, disable_number_display=False),  
        sg.T('    1', key='_RIGHT_')], 
        [sg.Text('Food Pairing:'), sg.Text('', key='_OUTPUT1_')],  
        [sg.Slider((1,100), key='_SLIDER2_', orientation='h', enable_events=True, disable_number_display=False),  
        sg.T('    1', key='_RIGHT2_')],
        [sg.Text('Number of People to Feed:'), sg.Text('', key='_OUTPUT2_')],  
        [sg.Slider((1,32), key='_SLIDER3_', orientation='h', enable_events=True, disable_number_display=False),  
        sg.T('    1', key='_RIGHT3_')],
        [sg.Button("Make a waffle recipe!"), sg.Exit()]]      

window = sg.Window('AI Waffle Chef', loadinglayout) # size=(800,600)
event, values = window.read(timeout=0)
# Here is where we will load the required models and data and such.
import time
time.sleep(4)
window.close()

window = sg.Window('AI Waffle Chef', layout) # size=(800,600)

while True:                             # The Event Loop
    event, values = window.read() 
    print(event, values)       
    if event in (None, 'Exit'):      
        break      
    window['_RIGHT_'].update(int(values['_SLIDER_']))  
    window['_RIGHT2_'].update(int(values['_SLIDER2_']))  
    window['_RIGHT3_'].update(int(values['_SLIDER3_']))  
window.close()
