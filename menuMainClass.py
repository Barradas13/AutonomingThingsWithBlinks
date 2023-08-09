import observerClasses
from observerClasses import DataEvent, Observable
import PySimpleGUI as sg
from observerClasses import Observer
import mouse


class Menu(Observer):
    def __init__(self):
        self.botoes = ['PRETO', 'AZUL', 'VERMELHO', 'VERDE', 'ROXO']
        self.botao_selecionado = -1
        self.window = None
        self.parar = False
        self.isAlive = True
        

    def create_layout(self):
        layout = [[sg.Button(button, key=f'button_{i}', button_color=('white', 'blue'), size=(12, 6)) for i, button in enumerate(self.botoes)], 
                  [sg.Button('QUADRADO', key='SQUARE', size=(69,14))]]
        return layout

    def run(self):
        self.window = sg.Window('MENU INTERAÇÃO FACIAL', self.create_layout(), size=(605, 400))

        while self.isAlive:
            event, values = self.window.read()
            if event in (sg.WINDOW_CLOSED, 'Exit') or self.parar:
                break

            for i, button in enumerate(self.botoes):
                if event == f'button_{i}':
                    self.selecionar_botao(button)
                    self.highlight_botaoSelecionado()
                    self.mostrar_prompt_interacao()
        print("trhead died")
        self.window.close()
        

    def selecionar_botao(self, button):
        self.botao_selecionado = self.botoes.index(button)

    def selecionar_botao_direita(self):
        # Função para selecionar o próximo botão.
        self.botao_selecionado = (self.botao_selecionado + 1) % len(self.botoes)
        print("")

    def interagir_botao_selecionado(self, tempo):
        selected_button = self.botoes[self.botao_selecionado]
        print(f'Interacting with {selected_button} button!')
        print(selected_button)
        if selected_button == 'PRETO':
            self.window[f'SQUARE'].update(button_color=('white', 'black'))
        elif selected_button == 'AZUL':
            self.window[f'SQUARE'].update(button_color=('white', 'blue'))
        elif selected_button == 'VERMELHO':
            self.window[f'SQUARE'].update(button_color=('white', 'red'))
        elif selected_button == 'VERDE':
            self.window[f'SQUARE'].update(button_color=('white', 'green'))
        elif selected_button == 'ROXO':
            self.window[f'SQUARE'].update(button_color=('white', 'purple'))
        return selected_button
    

    def mostrar_prompt_interacao(self):
        selected_button = self.botoes[self.botao_selecionado]
        print(f'Selected {selected_button} button!')
        return selected_button

    def highlight_botaoSelecionado(self):
        for i, button in enumerate(self.botoes):
            if i == self.botao_selecionado:
                self.window[f'button_{i}'].update(button_color=('white', 'green'))
            else:
                self.window[f'button_{i}'].update(button_color=('white', 'blue'))


    def update(self,  subject: Observable, dataEvent: DataEvent) -> None:
        try:
            if dataEvent.piscou and dataEvent.tempo <= 1.5:
                self.selecionar_botao_direita()
                self.highlight_botaoSelecionado()
                self.mostrar_prompt_interacao()
            elif dataEvent.piscou and dataEvent.tempo > 1.5:
                self.interagir_botao_selecionado(dataEvent.tempo)
                self.mostrar_prompt_interacao()
            elif not dataEvent.piscou and not dataEvent.tempo:
                self.isAlive = False
                print("chamou")
                self.window.close()
                self.parar = True
                
        except AttributeError:
            pass