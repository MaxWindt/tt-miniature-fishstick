_S='placeholder_rooms'
_R='DE/EN - Martin - clbuk'
_Q='EN - Isabella - 627rt'
_P='DE - Klaus - 166en'
_O='DE/EN - Sabine - 1765z'
_N='DE/EN - Kohl - a5k6y'
_M='DE - Pegasus - 6y1rf'
_L='NT - Antonio - 263zt'
_K='DE - Carlos - 6qo39'
_J='EN - Maria - 8iucm'
_I='DE - Jennifer - 2nlj4'
_H='DE - Alejandro - ny3sy'
_G='DE/EN - Javier - 1i0vz'
_F='This list shows you Participants in breakout rooms. By checking a row you can save this setting so it will not change in the refreshing process.'
_E='NT - Dieter - q9nrw'
_D='EN - John - ucl01'
_C='DE/EN - Ashley - pxgmw'
_B=False
_A=True
import os,flet as ft
from open_breakout_rooms import create_groups,breakout_assignment
import utils,numpy as np,time
monitor_running=_A
testmode=_B
participant_list=[]
fixed_participants=[]
def stop_monitor():A=_B
def get_language_of_group(list_of_participants):
	D='2';C='1';B=list_of_participants
	def J(id):
		A={C:0,D:0}
		for E in B[B[:,0]==id]:
			if'DE'in E[2]:A[C]+=1
			elif'EN'in E[2]:A[D]+=1
		if A[C]==0:return D
		elif A[D]==0:return C
		F=sorted(A.items(),key=lambda x:x[1]);return F[1][0]+F[0][0]
	K=np.array([J(id)for id in B[:,0]]);E=np.column_stack((B[:,:1],K,B[:,1:]));E=np.unique(E[:,:3],axis=0);L=sorted(E,key=lambda x:int(x[2]));M=[A for A in L if A[2]!='3'];F=[];G=[];H=[];I=[]
	for A in M:
		if A[1]==C:F.append(A)
		elif A[1]==D:G.append(A)
		elif A[1]=='21':H.append(A)
		elif A[1]=='12':I.append(A)
	N=[F,G,I,H];return N
t=ft.Text(_F)
def on_participant_select(e):
	'\n    When a participant is selected in the autocomplete, this function is called.\n    The Data Row is then selected\n\n    :param e: The event that triggered this function\n    ';A=e.control
	for C in range(10):
		if hasattr(A,'selected'):B=A;break
		A=A.parent
	if not B.selected:B.selected=_A;update_fixed_participants(B)
	e.page.update()
def participant_selector(page,selected_participant,participant_list):
	A=selected_participant
	def F(_):C=B.value.lower();A=[A for A in participant_list if C in A.lower()];D.controls=[ft.TextButton(content=ft.Row([ft.Text(value=A,size=15,width=150)],alignment=ft.MainAxisAlignment.START),on_click=J,style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)))for(B,A)in enumerate(A)];D.update()
	def J(e):A.value=e.control._TextButton__content._Row__controls[0].value;I.update();on_participant_select(e);G(None)
	def G(_):E.open=_B;page.update()
	def K(_):B.value='';F(None);E.open=_A;page.update()
	A=ft.Text(A,size=13,height=40,expand=_A);H=ft.Icon(ft.icons.EDIT,visible=_B,size=20);I=ft.Row([H,A]);C=ft.Container(content=I,on_click=K,padding=5,alignment=ft.alignment.center)
	def L(e):H.visible=e.data=='true';C.update()
	C.on_hover=L;B=ft.TextField(label='Search names');D=ft.ListView();E=ft.AlertDialog(title=ft.Text('Find participant'),content=ft.Column([B,D],tight=_A,scroll=ft.ScrollMode.AUTO,expand=_A),actions=[ft.TextButton('Cancel',on_click=G)],actions_alignment=ft.MainAxisAlignment.END);B.on_change=F;return ft.Column([C,E],alignment=ft.alignment.center)
def update_fixed_participants(control):
	A=control;global fixed_participants;C=A._DataRow__cells[0]._DataCell__content.value;B=A._DataRow__cells[1]._DataCell__content._Column__controls[0]._Container__content._Row__controls[1].value
	if A.selected:fixed_participants.append([C,B])
	else:fixed_participants=[A for A in fixed_participants if A[1]!=B];print(fixed_participants)
def on_select_changed(e):A=e.control;A.selected=not e.control.selected;update_fixed_participants(A);e.page.update()
def create_room_nr_input(room_nr):return ft.CupertinoTextField(dense=_A,value=room_nr,width=40,max_length=3,text_align=ft.TextAlign.CENTER,input_filter=ft.InputFilter(regex_string='^[0-9]*$'))
def get_all_cell_values(data_table):
	C=[]
	for D in data_table.rows:
		A=[]
		for B in D.cells:
			if hasattr(B.content,'value'):E=B.content.value;A.append(E)
			else:F=B._DataCell__content._Column__controls[0]._Container__content._Row__controls[1].value;A.append(F)
		C.append(A)
	return C
async def initiate_breakout_room_table(page,webSDK_page):
	global breakout_room_table;global fixed_participants
	if testmode:A=[_C,_G,_D,_H,_I,_E,_J,_K,_L,_M,_N,_O,_P,_Q,_R]
	else:F=await utils.web_getBreakoutRooms(webSDK_page);A=[A['displayName']for A in F['unassigned']]
	G=utils.get_settings_file();B,I,J=await create_groups(A,G,fixed_participants);print(B);breakout_room_table.rows.clear()
	for C in enumerate(B,start=1):
		D=C[1][0];E=C[1][1];H=ft.DataRow(on_select_changed=on_select_changed,cells=[ft.DataCell(create_room_nr_input(D)),ft.DataCell(participant_selector(page,E,A))]);breakout_room_table.rows.append(H)
		if[D,E]in fixed_participants:breakout_room_table.rows[-1].selected=_A
	page.update()
breakout_room_table=ft.DataTable(sort_column_index=0,sort_ascending=_A,column_spacing=0,checkbox_horizontal_margin=3,divider_thickness=0,columns=[ft.DataColumn(ft.Row(alignment=ft.MainAxisAlignment.CENTER,controls=[ft.Icon(name=ft.icons.MEETING_ROOM)]),on_sort=lambda e:sort_table(e,0)),ft.DataColumn(ft.Row(alignment=ft.MainAxisAlignment.CENTER,controls=[ft.Icon(name=ft.icons.PERSON)]),on_sort=lambda e:sort_table(e,1))],rows=[],show_checkbox_column=_A)
def filter_rows(search_term):
	B=search_term
	for A in breakout_room_table.rows:C=str(A.cells[0].content.value);D=A.cells[1].content._Column__controls[0]._Container__content._Row__controls[0].value.lower();A.visible=B.lower()in C or B.lower()in D
def clear_search(e):search_field.value='';search_field.update();filter_rows('');breakout_room_table.update()
def on_search_change(e):filter_rows(search_field.value);breakout_room_table.update()
def sort_table(e,column_index):A=column_index;breakout_room_table.sort_column_index=A;breakout_room_table.sort_ascending=not breakout_room_table.sort_ascending if breakout_room_table.sort_column_index==A else _A;breakout_room_table.rows.sort(key=lambda x:x.cells[A].content.value if A==0 else x.cells[A].content._Column__controls[0]._Container__content._Row__controls[0].value,reverse=not breakout_room_table.sort_ascending);breakout_room_table.update()
async def create_pagelet(page,webSDK_page):
	A=webSDK_page;global breakout_room_table,search_field;E=[]
	async def B(e):await initiate_breakout_room_table(e.page,A)
	C=ft.Text(_F);search_field=ft.TextField(label='Search',on_change=on_search_change,expand=_A,dense=_A,suffix=ft.IconButton(ft.icons.CLOSE,on_click=clear_search));D=ft.IconButton(icon=ft.icons.REFRESH,icon_size=20,tooltip='Refresh Participants',on_click=B);F=ft.IconButton(icon=ft.icons.SETTINGS,icon_size=20,tooltip='Jump To Settings');G=ft.PopupMenuButton(items=[ft.PopupMenuItem(text='Item 1'),ft.PopupMenuItem(icon=ft.icons.POWER_INPUT,text='Check power'),ft.PopupMenuItem(content=ft.Row([ft.Icon(ft.icons.HOURGLASS_TOP_OUTLINED),ft.Text('Item with a custom content')]),on_click=lambda _:print('Button with a custom content clicked!'))]);H=ft.Row(controls=[search_field,D,F,G],alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
	async def I(e):
		D=get_all_cell_values(breakout_room_table);print(D);B=utils.get_settings_file();I,F,G=await create_groups(E,B);C=await utils.web_getBreakoutRooms(A)
		if C['rooms']:await utils.web_remove_all_rooms(A)
		await utils.create_rooms(A,F,G,B);C=await utils.web_getBreakoutRooms(A);await breakout_assignment(D,B[_S],C,A);H={'isAutoJoinRoom':_B,'isBackToMainSessionEnabled':_A,'isTimerEnabled':_A,'timerDuration':360,'notNotifyMe':_B,'needCountDown':_A,'waitSeconds':30};await utils.web_openBreakoutRooms(A,H)
	J=ft.Pagelet(content=ft.Column(scroll=ft.ScrollMode.AUTO,expand=_A,controls=[C,H,breakout_room_table]),floating_action_button=ft.FloatingActionButton(icon=ft.icons.STREAM,on_click=I,tooltip='Open Breakout Rooms'),width=300);await initiate_breakout_room_table(page,A);return J
def main(page):
	A=page;A.window.width=300;A.window.min_width=300;A.window.max_width=300
	async def B():B={'group_size':3,'minimal_group':2,_S:3,'activate_language1':_A,'activate_language2':_A,'add_universal_to_language1':_A,'add_universal_to_language2':_A,'tags_nt':['Triad','TRIAD','NT','triad','tirad','^nt '],'tags_hosts':['Host','\\.:\\.','Team'],'tags_lang1':['DE','De-','De ','^de ','^de-','^de/','D E '],'tags_lang2':['EN','En-','En ','ES','SP'],'version':'beta 0.3.1'};C=[_C,_G,_D,_H,_I,_E,_J,_K,_L,_M,_N,_O,_P,_Q,_R];D=await create_groups(C,B,preset_assignments=[[13,_C],[13,_E],[11,_D]]);A.add(ft.Container(content=ft.Column([await create_pagelet(A,None)],spacing=0,scroll=ft.ScrollMode.ALWAYS,expand=_A),padding=ft.padding.symmetric(vertical=0)))
	import asyncio as C;C.run(B())
if __name__=='__main__':ft.app(target=main)