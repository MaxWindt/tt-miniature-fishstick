_M='unassigned'
_L='tags_lang2'
_K='tags_lang1'
_J='tags_hosts'
_I='tags_nt'
_H='add_universal_to_language2'
_G='add_universal_to_language1'
_F='activate_language2'
_E='activate_language1'
_D='minimal_group'
_C='group_size'
_B='placeholder_rooms'
_A=True
import re,time,numpy as np,utils
def find_name(participant_list,name):
	A=[]
	for B in range(len(name)):C=re.compile(name[B]);D=list(filter(C.findall,participant_list));A.extend(D)
	return np.unique(A)
def shuffle(array):A=np.random.default_rng().permuted(array);return A
def split_into_groups_of(lst,group_size):
	B=lst;A=group_size
	if B.size!=0:C=len(B)%A;F=A-C if C!=0 else 0;D=np.concatenate((np.full(F,''),B));E=np.split(D,len(D)/A)
	else:E=[np.full(A,'')]
	return E
async def create_groups(participant_list,settings,preset_assignments=[]):
	J=preset_assignments;C=participant_list;A=settings;global group_size;global minimal_group;global placeholder_rooms;global toggle_language;global add_universal_to_language;global tags_nt;global tags_hosts;global tags_lang1;global tags_lang2;U={B:A for(A,B)in J};F=[A for(B,A)in J];C=[A for A in C if A not in F];group_size=A[_C];minimal_group=A[_D];placeholder_rooms=A[_B];V=A[_E];W=A[_F];add_universal_to_language=[A[_G],A[_H]];tags_nt=A[_I];tags_hosts=A[_J];tags_lang1=A[_K];tags_lang2=A[_L];K=find_name(C,tags_nt);L=find_name(C,tags_hosts);N=find_name(C,tags_lang1);O=find_name(C,tags_lang2);G=np.intersect1d(N,O);H=np.setdiff1d(N,np.concatenate((G,K,L)));E=np.setdiff1d(O,np.concatenate((G,K,L)));X=np.setdiff1d(C,np.concatenate((G,K,L,H,E)));P=np.concatenate((G,X));F=[A[1]for A in J];H=np.setdiff1d(H,F);E=np.setdiff1d(E,F);P=np.setdiff1d(P,F)
	if np.sum(add_universal_to_language)!=0:Q=np.array_split(shuffle(P),np.sum(add_universal_to_language))
	if add_universal_to_language[0]:D=np.concatenate((H,Q[0]))
	else:D=H
	if add_universal_to_language[1]:
		if np.sum(add_universal_to_language)==1:B=np.concatenate((E,Q[0]))
		elif np.sum(add_universal_to_language)==2:B=np.concatenate((E,Q[1]))
	else:B=E
	D=shuffle(D);B=shuffle(B)
	for(S,I)in J:
		if I in N or I in G:R=min(S-1,len(D));D=np.insert(D,R,I)
		elif I in O:R=min(S-1,len(B));B=np.insert(B,R,I)
	T=split_into_groups_of(D,group_size);Y=split_into_groups_of(B,group_size);M=[]
	if V:M.extend(T)
	if W:M.extend(Y)
	Z=len(T);a=len(M);b=utils.merge_hosts_notriad_participants(L,K,M,A[_B],U,group_size);return b,Z,a
async def breakout_assignment(participants_in_rooms,placeholder_rooms,Breakout_Rooms_Info,page):
	D=Breakout_Rooms_Info;G=D[_M];A=0;E=[]
	for F in enumerate(participants_in_rooms):
		B=int(F[1][0])
		if B not in E:
			C=F[1][1];H=D['rooms'][B-1]['boId']
			if C and isinstance(C,str):I=utils.find_participantID(C,G);await utils.web_assign_user_to_breakout_room(page,H,I);A=0
			else:
				A=A+1
				if group_size-A<minimal_group:E.append(B)
async def main(page,settings):
	E=False;C=settings;A=page;F=time.time();G=time.time();B=await utils.web_getBreakoutRooms(A)
	if B['rooms']:await utils.web_remove_all_rooms(A);B=await utils.web_getBreakoutRooms(A)
	H=[A['displayName']for A in B[_M]];D,I,J=await create_groups(H,C);await utils.create_rooms(A,I,J,C);B=await utils.web_getBreakoutRooms(A);await breakout_assignment(D,placeholder_rooms,B,A);K={'isAutoJoinRoom':E,'isBackToMainSessionEnabled':_A,'isTimerEnabled':_A,'timerDuration':360,'notNotifyMe':E,'needCountDown':_A,'waitSeconds':30};utils.web_openBreakoutRooms(A,K);L=time.time()-F;M=time.time()-G;print(L);print(M);print(D)
if __name__=='__main__':
	async def test():C='NT - Dieter - q9nrw';B='EN - John - ucl01';A='DE/EN - Ashley - pxgmw';D={_C:3,_D:2,_B:3,_E:_A,_F:_A,_G:_A,_H:_A,_I:['Triad','TRIAD','NT','triad','tirad','^nt '],_J:['Host','\\.:\\.','Team'],_K:['DE','De-','De ','^de ','^de-','^de/','D E '],_L:['EN','En-','En ','ES','SP'],'version':'beta 0.3.1'};E=[A,'DE/EN - Javier - 1i0vz',B,'DE - Alejandro - ny3sy','DE - Jennifer - 2nlj4',C,'EN - Maria - 8iucm','DE - Carlos - 6qo39','NT - Antonio - 263zt','DE - Pegasus - 6y1rf','DE/EN - Kohl - a5k6y','DE/EN - Sabine - 1765z','DE - Klaus - 166en','EN - Isabella - 627rt','DE/EN - Martin - clbuk'];F=await create_groups(E,D,preset_assignments=[[13,A],[13,C],[11,B]]);print(F)
	import asyncio;asyncio.run(test())