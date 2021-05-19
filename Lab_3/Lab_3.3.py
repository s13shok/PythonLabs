import wx
import re
import os
import datetime

class LogFrame(wx.Frame):

    def __init__(self):
        wx.Frame.__init__(self, None, -1, 'Искатель строк', size=(500, 400))
        self.create_menu()
        self.statusbar = self.CreateStatusBar()
        self.statusbar.SetFieldsCount(2)
        self.statusbar.SetStatusWidths([-3, -2])
        self.create_log_file()

        self.sample_list = []
        self.list_box = wx.ListBox(self, -1, (20, 20), (80, 120), self.sample_list, wx.LB_SINGLE)

        self.statusbar.SetStatusText('')
        self.statusbar.SetStatusText('', 1)

    def create_log_file(self):
        log_path = os.path.join(os.path.dirname(__file__), 'script18.log')
        if not os.path.exists(log_path):
            message = wx.MessageDialog(self,'Файл лога не найден. Файл будет создан автоматически')
            message.ShowModal()
            with open(log_path,'w') as f:
                pass


    def menu_data(self):
        data = (('&Файл',
                 ({'&Открыть...': self.open_file},)),
                ('&Лог',
                 ({'&Экспорт...': self.save_log},
                  {'&Добавить в лог': self.add_to_log},
                  {'&Просмотр лога': self.read_log})
                 ))
        return data

    def create_menu(self):
        menu = wx.MenuBar()

        for item in self.menu_data():
            menu_item = self.create_sub_menu(item[1])
            menu.Append(menu_item, item[0])

        self.SetMenuBar(menu)

    def create_sub_menu(self, itemgroup):
        groupmenu = wx.Menu()
 
        for items in itemgroup:
            for item in items.keys():
                title = item
                handler = items[item]
                menu_item = groupmenu.Append(-1, title)
                if handler:
                    self.Bind(wx.EVT_MENU, handler, menu_item)

        return groupmenu

    def open_file(self, event):
        dlg = wx.FileDialog(self, message='Выберите файл', defaultDir='', defaultFile='', wildcard='*.*', style=wx.FD_OPEN)

        # при открытии файла просто обновляем строку состояния
        if dlg.ShowModal() == wx.ID_CANCEL:
            return  

        self.statusbar.SetStatusText(f'Обработан файл {dlg.GetPath()}')
        size = f'{os.path.getsize(dlg.GetPath()):,}'.replace(',',' ')
        self.statusbar.SetStatusText(f'{size} байт',1)
        self.find_matches(self.get_text(dlg.GetPath()), dlg.GetPath())
        
    def get_text(self, name):
        try:
            with open (name, 'r') as f:
                return f.readlines()
        except IOError as err:
            print(err)
            return []

    def find_matches(self, lines, path):
        regex = r':?-?\)+' # :)  :))  ))))
        self.list_box.InsertItems([f'Файл {path} был обработан {datetime.datetime.now()}\n', '\n'], self.list_box.GetCount())
        line_number = 1
        for i in lines:
            data = [f'Строка {line_number:2}, позиция {match.start():2}: найдено \'{match.group():2}\'\n' for match in re.finditer(regex, i)]
            if len(data)!=0:
                self.list_box.InsertItems(data, self.list_box.GetCount())
            line_number+=1
        self.list_box.InsertItems(['\n'], self.list_box.GetCount())

    def save_log(self, event):
        dlg = wx.FileDialog(self, message='Выберите файл', defaultDir='', defaultFile='', wildcard='*.*', style=wx.FD_SAVE)
        if dlg.ShowModal() != wx.ID_CANCEL:
            with open(dlg.GetPath(),'w') as f:
                f.writelines(self.list_box.Items)
        
    def add_to_log(self, event):
        log_path = os.path.join(os.path.dirname(__file__), 'script18.log')
        with open(log_path,'a') as f:
            f.writelines(self.list_box.Items)

    def read_log(self, event):
        dlg = wx.MessageDialog(self,'Вы действительно хотите открыть лог? Данные последних поисков будут потеряны!','Warning', wx.OK | wx.CANCEL)
        dlg.SetOKCancelLabels('Да','Нет')
        
        if dlg.ShowModal() == wx.ID_OK:
            log_path = os.path.join(os.path.dirname(__file__), 'script18.log')
            text = []
            with open (log_path,'r') as f:
                text = f.readlines() 
            self.list_box.Clear()
            self.list_box.InsertItems(text, 0)
        return
        

if __name__ == '__main__':
    # создаем объект приложения
    app = wx.App()
    # создаем объект окна MainFrame
    log_frame = LogFrame()
    # и показываем
    log_frame.Show()
    # запускаем главный цикл обработки сообщений
    app.MainLoop()