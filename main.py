_G='settings.txt'
_F='Fadeout'
_E='min'
_D=None
_C='00:00'
_B=False
_A=True
import asyncio,subprocess,sys,os,time,flet as ft,yaml,webbrowser
from gui_breakout_monitor import create_pagelet,testmode
import utils,open_breakout_rooms
from playwright.async_api import async_playwright,expect
__version__=utils.__version__
development_mode=_B
SDK_URL='https://triad-tool-backend-thrumming-tree-4150.fly.dev'
t_rounds=ft.TextField(value=3,width=50,text_align=ft.TextAlign.CENTER)
t_checkin=ft.TextField(value=2,width=80,label='CheckIn',label_style=ft.TextStyle(size=15),suffix_text=_E)
t_round_duration=ft.TextField(value=3,width=80,label='Round',label_style=ft.TextStyle(size=15),suffix_text=_E)
t_fadeout=ft.TextField(value=2,width=80,label=_F,label_style=ft.TextStyle(size=14),suffix_text=_E)
l_total_time=ft.Text(value='--:--',size=15)
pb=ft.ProgressBar(width=210,value=1)
global t_info
t_info=ft.Text('',size=20)
t_currenttime=ft.Text(_C,size=50)
c_ring_bell=ft.Switch(label='Ring bell in main room',value=_A)
c_send_to_breakouts=ft.Switch(label='Send text to sessions',value=_A)
t_send_to_breakouts=ft.TextField(value='{i}. person can start now ∞ {i}. Person kann jetzt beginnen')
t_send_to_breakouts_fadeout=ft.TextField(value='Fadeout ∞ Ausklingen')
email='max@thesharing.space'
webSDK_page=_D
def safe_settings(e):
	A=utils.get_settings_file();A['group_size']=int(dd_group_size.value)
	with open(_G,'w')as B:yaml.dump(A,B,sort_keys=_B,default_flow_style=_B)
	t_rounds.value=dd_group_size.value;t_rounds.update()
dd_group_size=ft.Dropdown(border='UNDERLINE',width=50,hint_text='Size',on_change=safe_settings,value=3,options=[ft.dropdown.Option(2),ft.dropdown.Option(3),ft.dropdown.Option(6)])
loading_breakout_monitor_content=ft.Container(content=ft.ProgressRing(),alignment=ft.alignment.center,height=300)
def toggle_sync(e):e.control.selected=not e.control.selected;print(e.control.selected);e.page.update()
c_sync_time_with_zoom=ft.IconButton(icon=ft.icons.SYNC_DISABLED,selected_icon=ft.icons.SYNC,selected=_A,on_click=toggle_sync)
async def gui(page):
	h='Enable Night Theme';g='??:??';f='user_inputs';e='c_sync_time_with_zoom';d='t_send_to_breakouts';c='t_send_to_breakouts_fadeout';b='dd_group_size';a='c_ring_bell';Z='c_send_to_breakouts';V='t_rounds';U='t_fadeout';T='t_round';S='t_checkin';H='red';J='timer_running';F='timer.json';A=page;A.title='Triad Tool';A.horizontal_alignment=ft.CrossAxisAlignment.CENTER;A.window.always_on_top=_A;A.window.width=300;A.window.min_width=300;A.window.max_width=400;D=ft.Text();K=ft.Tab();E=ft.SnackBar(content=D,action='OK');A.overlay.append(E);C=ft.Audio(src='zimbeln.mp3');A.overlay.append(C)
	async def W():B={S:t_checkin.value,T:t_round_duration.value,U:t_fadeout.value,V:t_rounds.value,Z:c_send_to_breakouts.value,a:c_ring_bell.value,b:dd_group_size.value,c:t_send_to_breakouts_fadeout.value,d:t_send_to_breakouts.value,e:c_sync_time_with_zoom.selected};await A.client_storage.set_async(f,B)
	async def i():B=await A.client_storage.get_async(f);t_checkin.value=B[S];t_round_duration.value=B[T];t_fadeout.value=B[U];t_rounds.value=B[V];c_send_to_breakouts.value=B[Z];c_ring_bell.value=B[a];dd_group_size.value=B[b];t_send_to_breakouts_fadeout.value=B[c];t_send_to_breakouts.value=B[d];c_sync_time_with_zoom.selected=B[e];A.update()
	try:await i()
	except:print('no user input saved yet')
	utils.save_listeners(F,{'open':_A})
	async def O():
		F='isHost';E='\n                        button => button.click()\n                        '
		try:
			if not testmode:
				global webSDK_page;G=await async_playwright().start();H=await G.chromium.launch(headless=_B,args=['--mute-audio --no-first-run --disable-sync --disable-extensions --disable-component-update --disable-background-networking']);I=await H.new_context(viewport={'width':420,'height':680},locale='en-US',permissions=[]);webSDK_page=await I.new_page();await webSDK_page.goto(SDK_URL);await webSDK_page.evaluate("startMeeting('3858026425', '1')")
				while _A:
					try:await expect(webSDK_page.get_by_label('Enter Full Screen')).to_be_visible(timeout=1000);B.disabled=_B;B.update();break
					except AssertionError:D='Failed to start web module. Check Internet Connection and creadentials.';A.controls[0].tabs[1].content=ft.Column([loading_breakout_monitor_content,ft.Text(D)]);A.update();print(D);await asyncio.sleep(2);print('Retrying...')
				try:await webSDK_page.get_by_label('More meeting control').evaluate(E);await webSDK_page.get_by_label('Stop Incoming Video').evaluate(E);print('Stopped incoming video');await utils.setup_active_speaker_spotlight(webSDK_page)
				except Exception:print('Stopping incoming video was not successful')
		except Exception as J:print(J);await O()
		try:
			C=await utils.web_getCurrentUser(webSDK_page)
			if F not in C or not C[F]and not C['isCoHost']:await webSDK_page.get_by_label('Reclaim Host').click(timeout=5000)
		except Exception:print('Something went wrong while claiming host rights...')
		A.controls[0].tabs[1].content=await create_pagelet(A,webSDK_page);A.update()
	def j(e):webbrowser.open(_G)
	def k(e):subprocess.run(sys.executable+' gui_breakout_monitor.py',shell=_A)
	def l(e):
		if K.selected_index!=0:A.floating_action_button.visible=_B;A.update();B.update();I(e)
		else:A.floating_action_button.visible=_A;A.update();B.update()
	async def m(e):
		global webSDK_page;await W();B.disabled=_A;B.update()
		try:await open_breakout_rooms.main(webSDK_page,utils.get_settings_file())
		except Exception as e:D.value=e;E.open=_A
		B.disabled=_B;A.update()
	B=ft.FloatingActionButton(icon=ft.icons.PLAY_ARROW,on_click=m,disabled=_A)
	def I(e):
		try:global checkin_duration;checkin_duration=int(t_checkin.value);t_checkin.border_color=_D;t_checkin.value=checkin_duration
		except:t_checkin.border_color=H
		try:global fadeout_duration;fadeout_duration=int(t_fadeout.value);t_fadeout.border_color=_D;t_fadeout.value=fadeout_duration
		except:t_fadeout.border_color=H
		try:global nr_of_rounds;nr_of_rounds=int(t_rounds.value);t_rounds.border_color=_D;t_rounds.value=nr_of_rounds
		except:t_rounds.border_color=H
		try:global round_duration;round_duration=int(t_round_duration.value);t_round_duration.border_color=_D;t_round_duration.value=round_duration
		except:t_round_duration.border_color=H
		try:B=(nr_of_rounds*round_duration+checkin_duration+fadeout_duration)*60;l_total_time.value=str(B//60)+':00'
		except:B=0;l_total_time.value=g
		A.update();return B
	async def R(text):
		B=text;global webSDK_page
		def F(e):C.open=_B;A.update();c_send_to_breakouts.value=_B
		C=ft.AlertDialog(modal=_A,title=ft.Text('Sending Text to Breakouts...'),content=ft.Text('Sending Text: \n'+B),actions=[ft.TextButton('STOP',on_click=F)],actions_alignment=ft.MainAxisAlignment.END);A.dialog=C;C.open=_A;A.update();await asyncio.sleep(3);C.open=_B;A.update()
		if c_send_to_breakouts.value:
			for H in range(3):
				if await utils.web_broadcastTextToBreakouts(webSDK_page,B):D.value='Text was send '+B;E.open=_A;A.update();return _A
				else:
					def G(e):A.banner.open=_B;A.update()
					A.banner=ft.Banner(bgcolor=ft.colors.AMBER_100,leading=ft.Icon(ft.icons.WARNING_AMBER_ROUNDED,color=ft.colors.RED,size=40),content=ft.Text('Text was not send!. Retrying... \n'+B),actions=[ft.TextButton('close',on_click=G)]);D.value='Text was not send!. Retrying...';A.banner.open=_A;A.update();await asyncio.sleep(3)
	def X():L.visible=_A;M.visible=_B;t_checkin.disabled=_B;t_fadeout.disabled=_B;t_round_duration.disabled=_B;t_rounds.disabled=_B;G.visible=_B;c_sync_time_with_zoom.visible=_A
	def n():L.visible=_B;M.visible=_A;t_checkin.disabled=_A;t_fadeout.disabled=_A;t_round_duration.disabled=_A;t_rounds.disabled=_A;G.visible=_A;c_sync_time_with_zoom.visible=_B
	def o():utils.save_listeners(F,{J:_A,'l_total_time':l_total_time.value,'pb':pb.value,'t_info':t_info.value,'t_currenttime':t_currenttime.value})
	def p(e):G.disabled=_A;utils.save_listeners(F,{J:_A});subprocess.run(sys.executable+' gui_timer_fullscreen.py',shell=_A);G.disabled=_B
	async def q(e):
		if l_total_time.value==g:D.value='Please check your inputs!';E.open=_A;A.update();return
		await W();G=I(e);utils.save_listeners(F,{J:_A});n();D.value='External audio shared?\nBreakout sessions window opened?';E.open=_A;A.update();B=0;global t_info;S=time.time();K=c_sync_time_with_zoom.selected;global webSDK_page
		try:
			if K:
				H=await utils.web_get_time_left_in_breakouts(A,E,webSDK_page)
				if H=='0':N=G
				else:
					N=int(H[0])*3600+int(H[1])*60+int(H[2])
					if G<N:N=G
				S=time.time()-(G-N);L=time.time()-S
				if L<=checkin_duration*60:O='Check-in';P=checkin_duration*60;T=0
				else:
					L-=checkin_duration*60;Z=L//(round_duration*60);U=L%(round_duration*60)
					if Z<nr_of_rounds:O='{i}. Person';P=round_duration*60;T=Z+1
					else:O=_F;P=fadeout_duration*60;T=t_rounds.value
				B=int(T);b=P-L%P
		except:K=_B;print('connection to zoom breakout window failed')
		while B<=t_rounds.value+2:
			V=time.time()
			if not K:
				if B==0:M=int(t_checkin.value);t_info.value='Check in'
				elif B==1:
					M=int(t_round_duration.value);t_info.value=f"{B}. Person"
					if c_send_to_breakouts.value:await R(t_send_to_breakouts.value.format(i=B))
					if c_ring_bell.value:C.play()
				elif B==t_rounds.value+1:
					M=int(t_fadeout.value);t_info.value=_F;A.update(t_info)
					if c_send_to_breakouts.value:await R(t_send_to_breakouts_fadeout.value)
					if c_ring_bell.value:C.play();await asyncio.sleep(4);C.play()
				elif B==t_rounds.value+2:
					M=0;A.update(t_info)
					if c_ring_bell.value:C.play();await asyncio.sleep(4);C.play();await asyncio.sleep(4);C.play()
				else:
					M=int(t_round_duration.value);t_info.value=f"{B}. Person"
					if c_ring_bell.value:C.play()
					if c_send_to_breakouts.value:await R(t_send_to_breakouts.value.format(i=B))
			if K:
				Q=V+b
				try:t_info.value=O.format(i=B)
				except:t_info.value=O
				K=_B
			else:Q=V+M*60
			if development_mode:Q=V+5
			A.update(t_info);B+=1
			while utils.read_listeners(F)[J]and time.time()<Q:
				c=S+G;U=Q-time.time();H=c-time.time();d=int(H//60);f=1-H/G;h=int(U//60);a=int(U%60);t_currenttime.value=f"{h:02d}:{a:02d}";l_total_time.value=f"{d:02d}:{a:02d}";pb.value=f;A.update();o();await asyncio.sleep(1)
				if not J in utils.read_listeners(F):B=t_rounds.value+1;G=0;t_currenttime.value=_C;l_total_time.value=_C;t_info.value='Stopped';X();A.update();return
		t_info.value='Finished';t_currenttime.value=_C;l_total_time.value=_C;Y(e);X();A.update()
	def Y(e):A=utils.read_listeners(F);utils.delete_t_value(A,J)
	t_rounds.on_change=I;t_checkin.on_change=I;t_round_duration.on_change=I;t_fadeout.on_change=I;L=ft.IconButton(icon=ft.icons.PLAY_ARROW_ROUNDED,on_click=q);M=ft.IconButton(icon=ft.icons.STOP,on_click=Y,visible=_B);G=ft.IconButton(icon=ft.icons.OPEN_IN_FULL,on_click=p,visible=_B);r=ft.Column(scroll=ft.ScrollMode.ALWAYS,height=A.height,controls=[ft.Row([t_info,t_currenttime],alignment=ft.MainAxisAlignment.CENTER),ft.Row([pb,l_total_time]),ft.Row([L,M,G,c_sync_time_with_zoom],alignment=ft.MainAxisAlignment.CENTER),ft.Row([t_checkin,t_round_duration,t_fadeout]),ft.Row([ft.Icon(ft.icons.GROUP),ft.Text('Rounds'),t_rounds],alignment=ft.MainAxisAlignment.CENTER),ft.ListTile(title=c_send_to_breakouts),ft.ListTile(title=c_ring_bell)])
	def s(e):A.theme_mode=ft.ThemeMode.DARK if A.theme_mode==ft.ThemeMode.LIGHT else ft.ThemeMode.LIGHT;P.label=h if A.theme_mode==ft.ThemeMode.LIGHT else'Return To Day Theme';A.update()
	A.theme_mode=ft.ThemeMode.LIGHT;P=ft.Switch(label=h,on_change=s)
	def Q(e):N.open=_B;A.update()
	def t(e):B='rcc.exe';print('Resetting Settings');A.client_storage.clear();utils.reset_settings_file();Q(e);A.window_close();os.execl(B,B,'run')
	N=ft.AlertDialog(modal=_A,title=ft.Text('Please confirm'),content=ft.Text('Do you really want to reset all settings?'),actions=[ft.TextButton('Yes',on_click=t),ft.TextButton('No',on_click=Q)],actions_alignment=ft.MainAxisAlignment.END,on_dismiss=lambda e:print('Modal dialog dismissed!'))
	def u(e):A.dialog=N;N.open=_A;A.update()
	v=ft.ElevatedButton('Reset Settings',icon='delete',icon_color=H,on_click=u);w=ft.Column(scroll=ft.ScrollMode.ALWAYS,spacing=0,controls=[ft.ExpansionTile(title=ft.Text('Timer',theme_style=ft.TextThemeStyle.TITLE_LARGE),affinity=ft.TileAffinity.LEADING,initially_expanded=_B,controls=[ft.ListTile(title=ft.Text('Switching to next person'),subtitle=t_send_to_breakouts),ft.ListTile(title=ft.Text('Fadeout started'),subtitle=t_send_to_breakouts_fadeout)]),ft.ExpansionTile(title=ft.Text('Other',theme_style=ft.TextThemeStyle.TITLE_LARGE),affinity=ft.TileAffinity.LEADING,initially_expanded=_A,controls=[ft.ListTile(title=P),ft.ListTile(title=v)])])
	def x(e):A.set_clipboard(email);D.value='Address Copied!';E.open=_A;A.update()
	async def y(e):global webSDK_page;await utils.trigger_listening_spotlight_active_speaker(webSDK_page)
	async def z(e):await utils.create_test_participants()
	K=ft.Tabs(selected_index=0,animation_duration=300,on_change=l,tabs=[ft.Tab(tab_content=ft.Icon(ft.icons.TIMER),content=r),ft.Tab(tab_content=ft.Icon(ft.icons.GROUPS),content=ft.Container(content=ft.Column([loading_breakout_monitor_content],spacing=0,scroll=ft.ScrollMode.ALWAYS,expand=_A),padding=ft.padding.symmetric(vertical=0))),ft.Tab(tab_content=ft.Icon(ft.icons.SETTINGS),content=ft.Column([ft.ListTile(leading=ft.Icon(ft.icons.GROUP),title=ft.Text('Group Size'),trailing=dd_group_size),ft.ListTile(leading=ft.Icon(ft.icons.MONITOR_HEART_OUTLINED),title=ft.Text('Room Monitor'),on_click=k),ft.ListTile(leading=ft.Icon(ft.icons.SETTINGS),title=ft.Text('Advanced Settings'),on_click=j),ft.ListTile(leading=ft.Icon(ft.icons.SETTINGS),title=ft.Text('spotlight_active_speaker'),on_click=y),w],scroll=ft.ScrollMode.ALWAYS,expand=_A)),ft.Tab(icon=ft.icons.INFO,content=ft.Column(controls=[ft.ListTile(title=ft.OutlinedButton(icon=ft.icons.GROUP_ADD,text='Add 5 Participants to Meeting',on_click=z)),ft.Text('Contact',size=18),ft.Text('If you have any questions or suggestions, please contact me at:'),ft.ListTile(url='mailto:max@thesharingspace.de',title=ft.Text('max@thesharingspace.de'),on_click=x),ft.Row([ft.Text('© 2022-'+str(time.gmtime(time.time()).tm_year)+' Max Schwindt'),ft.IconButton(icon=ft.icons.CODE,url='https://github.com/MaxWindt/zoom-triad-tool')]),ft.Text('Version: '+__version__)],alignment=ft.CrossAxisAlignment.CENTER))],width=400,expand=_A);A.floating_action_button=B;A.add(K);A.run_task(O)
ft.app(target=gui)