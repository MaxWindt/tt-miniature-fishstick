import os,time,flet as ft,tkinter as tk,utils
def get_screen_resolution():A=tk.Tk();B=A.winfo_screenwidth();C=A.winfo_screenheight();A.destroy();return B,C
screen_width,screen_height=get_screen_resolution()
l_total_time=ft.Text(value='--:--',size=15)
pb=ft.ProgressBar(width=210,value=1)
t_info=ft.Text('',size=20)
t_currenttime=ft.Text('00:00',size=50)
original_width=300
def main(page):
	C='timer.json';A=page;A.title='Timer'
	def D(e):B=A.window.width/original_width;l_total_time.size=int(15*B);pb.width=int(210*B);pb.height=int(4*B);t_info.size=int(20*B);t_currenttime.size=int(50*B);A.update()
	A.window_frameless=True;A.window.width=screen_width;A.window_height=screen_height;A.on_resize=D;A.add(ft.Column(scroll=ft.ScrollMode.ALWAYS,height=A.height,controls=[ft.Row([t_info,t_currenttime],alignment=ft.MainAxisAlignment.CENTER),ft.Row([pb,l_total_time],alignment=ft.MainAxisAlignment.CENTER)]));A.update()
	while os.path.isfile(utils.temp_settings_filename)and'timer_running'in utils.read_listeners(C):
		time.sleep(1)
		try:B=utils.read_listeners(C);l_total_time.value=B['l_total_time'];pb.value=B['pb'];t_info.value=B['t_info'];t_currenttime.value=B['t_currenttime'];A.update()
		except:print('Timer not running')
	A.window_destroy()
if __name__=='__main__':ft.app(target=main)