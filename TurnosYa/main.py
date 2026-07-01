import wx
import wx.adv
import os

app = wx.App()

#Cargar Splash

ruta_img = os.path.join(os.path.dirname(os.path.abspath(__file__)),"LogoTurnosYa.png")

bitmap = wx.Bitmap(ruta_img)

splash = wx.adv.SplashScreen(
    bitmap,
    wx.adv.SPLASH_CENTRE_ON_SCREEN | wx.adv.SPLASH_TIMEOUT,
    2000,
    None,
    -1
)

wx.Yield()

#Fuentes

fuente1 = wx.Font(
    16,
    wx.FONTFAMILY_DEFAULT,
    wx.FONTSTYLE_NORMAL,
    wx.FONTWEIGHT_BOLD
)

fuente2 = wx.Font(
    13,
    wx.FONTFAMILY_DEFAULT,
    wx.FONTSTYLE_NORMAL,
    wx.FONTWEIGHT_BOLD
)

fuente3 = wx.Font(
    28,
    wx.FONTFAMILY_DEFAULT,
    wx.FONTSTYLE_NORMAL,
    wx.FONTWEIGHT_BOLD
)


class MyFrame(wx.Frame):
    def __init__(self, parent, title,):
        estilo=wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX | wx.MINIMIZE_BOX
        super(MyFrame, self).__init__(parent, title=title, size=(550, 450), style= estilo)
        self.CenterOnScreen()

        #Icono de la app

        icon_path = r"C:\Users\tomas\OneDrive\Documentos\Codigos\TurnosYa\TY_icono.ico"
        icon = wx.Icon(icon_path, wx.BITMAP_TYPE_ICO)
        self.SetIcon(icon)

        #Inicializar variables
        self.servicio = None
        self.horario = None
        self.fecha = None

        #Panel principal
        panel = wx.Panel(self)

        #Instanciar Notebook
        notebook = wx.Notebook(panel)

        #Crear paneles
        inicio = wx.Panel(notebook)
        sacarTurno = wx.Panel(notebook)
        historial = wx.Panel(notebook)
        

        #Color de las Pestañas
        inicio.SetBackgroundColour(wx.Colour(43, 175, 181))
        sacarTurno.SetBackgroundColour(wx.Colour(43, 175, 181))
        historial.SetBackgroundColour(wx.Colour(43, 175, 181))
        
        #Botones

        botonTurno = wx.Button(sacarTurno, -1, "Elegir Servicio", pos=(20,10), size=(140,60))
        botonHorario = wx.Button(sacarTurno, -1, "Elegir Horario", pos=(200,10), size=(140,60))
        botonGuardar = wx.Button(sacarTurno, -1, "Guardar Turno", pos=(365,10), size=(140,90))

        #Modificaciones a botones
        botonTurno.Bind(wx.EVT_BUTTON, self.TipoTurno)
        botonTurno.SetFont(fuente2)
        botonHorario.Bind(wx.EVT_BUTTON, self.Horario)
        botonHorario.SetFont(fuente2)
        botonGuardar.SetFont(fuente2)
        botonGuardar.Bind(wx.EVT_BUTTON, self.Guardar)

        #Textos
        self.lbl_seleccion = wx.StaticText(sacarTurno, label="Fecha seleccionada: ", pos=(20, 350))
        textoFecha = wx.StaticText(sacarTurno, label= "Seleccione la fecha del turno", pos=(108, 110))
        textoFecha.SetFont(fuente1)
        self.textoServicio = wx.StaticText(sacarTurno, label= "Todavía no elegiste un servicio", pos= (10,80))
        self.textoHorario = wx.StaticText(sacarTurno, label= "Todavía no elegiste horario", pos= (200,80))
        textoBienvenida = wx.StaticText(inicio, label= "BIENVENIDO A TURNOSYA", pos=(20,40))
        self.textoUltimoTurno = wx.StaticText(inicio,label="Cargando...",pos=(20,120))
        self.textoUltimoTurno.SetFont(fuente2)
        textoBienvenida.SetFont(fuente3)
        self.listaHistorial = wx.ListBox(historial,pos=(15, 30),size=(490, 330))
        textoHistorial = wx.StaticText (historial,label=("Historial de Turnos"),pos=(20,5))
        textoHistorial.SetFont(fuente1)


        #Crear el control de Calendario
        self.calendario = wx.adv.CalendarCtrl(sacarTurno, id=wx.ID_ANY, pos=(8, 140), size=(500,200))
        self.calendario.Bind(wx.adv.EVT_CALENDAR_SEL_CHANGED, self.AlSeleccionarFecha)
        

        #Añadir los paneles al Notebook con su etiqueta
        notebook.AddPage(inicio, "Inicio")
        notebook.AddPage(sacarTurno, "Sacar Turno")
        notebook.AddPage(historial, "Historial")

        #Organizar el layout para que el Notebook ocupe todo el espacio
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(notebook, 1, wx.EXPAND | wx.ALL, 5)
        panel.SetSizer(sizer)


        self.CargarUltimoTurno()
        self.CargarHistorial()

        self.Show()

    #Funcion para elegir el dia del turno

    def AlSeleccionarFecha(self, evento):
       fecha = evento.GetDate()
       self.fecha = fecha.Format("%d / %m / %Y")

       print(self.fecha)
       self.lbl_seleccion.SetLabel(f"Fecha seleccionada: {self.fecha}")

    #Funcion para elegir el tipo de servicio

    def TipoTurno(self, evt):
        dlg = wx.TextEntryDialog(
                self, 'Escribi para que queres sacar turno',
                'Tipo de Turno')

        if dlg.ShowModal() == wx.ID_OK:
            self.servicio = dlg.GetValue()
            print(self.servicio)
            self.textoServicio.SetLabel(self.servicio)

    #Funcion para elegir la hora del turno

    def Horario(self, evt):
        dlg = wx.Dialog(self, title="Elegir Horario", size=(250,150))
        panel = wx.Panel(dlg)
        timepicker = wx.adv.TimePickerCtrl(
            panel,
            pos=(40, 20),
            size=(120, -1)
        )
        btn_ok = wx.Button(panel, wx.ID_OK, "OK", pos=(80, 60))

        if dlg.ShowModal() == wx.ID_OK:
            hora, minuto, _ = timepicker.GetTime()

            self.horario = f"{hora:02d}:{minuto:02d}"
            print(self.horario)
            self.textoHorario.SetLabel(self.horario)
            
    #Funcion para guardar el turno

    def Guardar(self, evt):
        if not self.servicio or not self.horario or not self.fecha:
            wx.MessageBox(
                "Tenés que elegir servicio, horario y fecha.",
                "Error",
                wx.OK | wx.ICON_WARNING
            )
            return

        ruta = os.path.join(os.path.dirname(os.path.abspath(__file__)), "historial.txt")

        with open(ruta, "a", encoding="utf-8") as archivo:  
            archivo.write(
                f"Servicio: {self.servicio} | "
                f"Fecha: {self.fecha} | "
                f"Horario: {self.horario}\n"
            )

        ultimo = (
        f"Servicio: {self.servicio} | "
        f"Fecha: {self.fecha} | "
        f"Horario: {self.horario}"
    )

        self.textoUltimoTurno.SetLabel(f"Último turno:\n{ultimo}")

        wx.MessageBox(
            "Turno guardado correctamente.",
            "Éxito",
            wx.OK | wx.ICON_INFORMATION
        )

    #Funcion para mostrar el ultimo turno agendado en el inicio

    def CargarUltimoTurno(self):
        ruta = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "historial.txt"
        )

        if not os.path.exists(ruta):
            self.textoUltimoTurno.SetLabel(
                "El último turno que sea guardado aparecerá acá"
            )
            return

        with open(ruta, "r", encoding="utf-8") as archivo:
            lineas = archivo.readlines()

        if len(lineas) == 0:
            self.textoUltimoTurno.SetLabel(
                "El último turno que sea guardado aparecerá acá"
            )
        else:
            ultimo = lineas[-1].strip()
            self.textoUltimoTurno.SetLabel(
                f"Último turno:\n{ultimo}"
            )
    
    #Funcion para guardar los turnos en el txt

    def CargarHistorial(self):
        ruta = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "historial.txt"
        )

        self.listaHistorial.Clear()

        if not os.path.exists(ruta):
            self.listaHistorial.Append("No hay turnos guardados.")
            return

        with open(ruta, "r", encoding="utf-8") as archivo:
            lineas = archivo.readlines()

        if not lineas:
            self.listaHistorial.Append("No hay turnos guardados.")
            return

        for linea in lineas:
            self.listaHistorial.Append(linea.strip())

MyFrame(None, "TurnosYa")
app.MainLoop()


