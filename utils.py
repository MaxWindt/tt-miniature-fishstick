_U='You need Co-Host rights to allow unmuting'
_T='Allow participants to unmute themselves unselect'
_S='Allow participants to unmute themselves selected'
_R="[id='particioantHostDropdown']"
_Q='open the manage participants'
_P='InProgress'
_O='result'
_N='Closed'
_M='height'
_L='--mute-audio'
_K='settings.txt'
_J='tags_lang2'
_I='tags_lang1'
_H='placeholder_rooms'
_G='displayName'
_F='Close'
_E=False
_D='More meeting control'
_C='button'
_B='\n                button => button.click()\n                '
_A=True
import os,subprocess,sys,asyncio
from playwright.async_api import async_playwright,expect
import json,yaml
__version__='beta 0.4.0'
temp_settings_filename='timer.json'
def save_listeners(filename,settings):
	with open(filename,'w')as A:json.dump(settings,A,indent=4)
def read_listeners(filename):
	try:
		with open(filename,'r')as A:return json.load(A)
	except FileNotFoundError:return{}
def reset_settings_file():
	A={'group_size':3,'minimal_group':2,_H:5,'activate_language1':_A,'activate_language2':_A,'add_universal_to_language1':_A,'add_universal_to_language2':_A,'tags_nt':['Triad','TRIAD','NT','triad','tirad','^nt '],'tags_hosts':['Host','\\.:\\.','Team'],_I:['DE','De-','De ','^de ','^de-','^de/','D E '],_J:['EN','En-','En ','ES','SP'],'version':__version__}
	with open(_K,'w')as B:yaml.dump(A,B,sort_keys=_E,default_flow_style=_E)
	return A
def get_settings_file():
	try:
		with open(_K)as B:A=yaml.safe_load(B)
	except:print('Error loading settings, loading defaults');A=reset_settings_file()
	return A
def delete_t_value(settings,tag):
	A=settings;del A[tag]
	with open(temp_settings_filename,'w')as B:json.dump(A,B)
def merge_hosts_notriad_participants(hosts,notriad,participants_in_groups,placeholder_rooms,preset_dict,group_size):
	K=group_size;J=participants_in_groups;I=hosts;G=placeholder_rooms;F=preset_dict;B=[];C=3+G;R=3+G+len(J);H={}
	for(D,A)in F.items():
		if A<C:A=C;C+=1
		H[A]=H.get(A,0)+1
	for(D,A)in F.items():
		if A<C:A=C;C+=1
		B.append([A,D])
	for(A,N)in H.items():
		for O in range(K-N):B.append([A,''])
	if any(I):B.append([1,I[0]])
	for(L,P)in enumerate(notriad):B.append([2,P])
	for L in range(G):B.append([3+L,''])
	E=C
	for Q in J:
		M=0
		for D in Q:
			if D not in F:
				while E in F.values():E+=1
				B.append([E,D]);M+=1
		for O in range(K-M):B.append([E,''])
		E+=1
	return sorted(B,key=lambda x:x[0])
def start_WebSDK_server():A=33833;B='WebSDK';D=subprocess.Popen([sys.executable,'-m','http.server',str(A),'--bind','127.0.0.1'],cwd=os.path.join(os.path.dirname(os.path.realpath(__file__)),B));C=f"http://localhost:{A}";print(f"Serving on {C}");print(f"Serving files from {B}");return D,C
async def install_browser():subprocess.run([sys.executable,'-m','playwright','install','chromium'],check=_A);print('Browser successfully installed')
async def TEST_start_web_module():
	A='\n            button => button.click()\n            ';global webSDK_page;F,B=start_WebSDK_server();install_browser();C=await async_playwright().start();D=await C.chromium.launch(headless=_E,args=[_L]);E=await D.new_context(viewport={'width':420,_M:680},locale='en-US',permissions=[]);webSDK_page=await E.new_page();await webSDK_page.goto(B);await expect(webSDK_page.get_by_label('Enter Full Screen')).to_be_visible(timeout=10000)
	try:await webSDK_page.get_by_label(_D).evaluate(A);await webSDK_page.get_by_label('Stop Incoming Video').evaluate(A);print('Stopped incoming video')
	except Exception:print('Stopping incoming video was not successful')
	try:await webSDK_page.get_by_label('Reclaim Host').click(timeout=5000)
	except Exception:print('already host')
	return webSDK_page
async def web_getCurrentUser(page):return await page.evaluate('() => {\n            return new Promise(resolve => {\n                ZoomMtg.getCurrentUser({\n                    success: function(res) {\n                        resolve(res.result.currentUser);\n                    },\n                });\n            });\n            }\n            ')
async def web_remove_all_rooms(page):
	C='Delete';B='Recreate';A=page;D=await web_getBreakoutRoomStatus(A)
	if D==_N:
		if not await A.get_by_label('Breakout Rooms Window').is_visible():await A.get_by_label(_D).evaluate('\n                    button => button.click()\n                    ');await A.get_by_label('Breakout Rooms').evaluate(_B)
		else:await A.get_by_role(_C,name=B).click();await A.get_by_label(B).fill('0');await A.get_by_text('Assign manually').click();await A.get_by_role(_C,name=B).click();await A.get_by_role('listitem').locator('div').first.hover();await A.get_by_role(_C,name=C).click();await A.get_by_label('Delete Room 1?').get_by_role(_C,name=C).press('Enter');await A.get_by_role(_C,name=_F).click()
	else:print('Cant clean the rooms, as breakout rooms are still running')
async def web_openBreakoutRooms(page,breakout_options):await page.evaluate('breakout_options => {\n            ZoomMtg.openBreakoutRooms({\n            options: breakout_options,\n            error: function (error) {\n                console.error("Error occurred:", error);\n            },\n            success: function (success) {\n                console.log("Here are the breakouts!", success);\n            },\n        });\n        }\n        ',breakout_options)
async def web_createBreakoutRooms(page,array):await page.evaluate('array => {\n            ZoomMtg.createBreakoutRoom({\n            data: array,\n            pattern: 3,\n            error: function (error) {\n                console.error("Error occurred:", error);\n            },\n            success: function (success) {\n                console.log("Here are the breakouts!", success);\n            },\n        });\n        }\n        ',array)
async def create_rooms(page,size_of_lang1,size_of_lang2,settings):
	C=settings;B=[];E=C[_I][0];F=C[_J][0];A=1;B.append('Teamroom');A+=1;B.append('No Triad');A+=1
	for D in range(C[_H]):B.append(f"Room {A}");A+=1
	for D in range(size_of_lang1):B.append(f"Room {A} {E}");A+=1
	for D in range(size_of_lang2):B.append(f"Room {A} {F}");A+=1
	for D in range(100-A):B.append(f"Room {A}");A+=1
	await web_createBreakoutRooms(page,B);return B
async def web_assign_user_to_breakout_room(page,target_room_id,user_id,success_callback=None,error_callback=None):A=user_id;A=int(A);return await page.evaluate('([targetRoomId, userId]) => {\n            ZoomMtg.assignUserToBreakoutRoom({\n                targetRoomId: targetRoomId,\n                userId: userId,\n                error: (error) => {\n                    console.error("Error occurred:", error);\n                    \n                },\n                success: (success) => {\n                    console.log("Here are the breakouts!", success);\n                },\n            });\n        }',[target_room_id,A])
async def web_getBreakoutRooms(page):await asyncio.sleep(1);A=await page.evaluate('() => {\n            return new Promise((resolve) => {\n                ZoomMtg.getBreakoutRooms({\n                    success: function(res) {\n                        resolve(res);\n                    },\n                    error: function (error) {\n                        console.log(error);\n                    },\n                });\n            });\n        }');return A[_O]
async def web_getBreakoutRoomStatus(page):
	B=await page.evaluate('() => {\n            return new Promise((resolve) => {\n                ZoomMtg.getBreakoutRoomStatus({\n                    success: function(res) {\n                        resolve(res);\n                    },\n                    error: function (error) {\n                        console.log(error);\n                    },\n                });\n            });\n        }');A=B[_O]['status']
	if A==2:A=_P
	elif A==3:A='Closing'
	elif A==4:A=_N
	return A
def extract_time_from_breakout_window_title(title):
	B=title
	try:
		C=B.find('(')
		if C!=-1:D=B.split('(');E=D[1].replace(')','');A=E.split(':')
		else:A='0'
	except Exception as F:A='0';print('breakout window is not open')
	return A
async def web_get_time_left_in_breakouts(page,snack_bar,webSDK_page):
	D=webSDK_page;A=snack_bar
	try:B=await web_getBreakoutRoomStatus(D)
	except Exception as F:B='WebSDK not ready';print(F)
	E=A.content
	if B==_P:
		G=await D.locator('div.bo-room-mgmt-window-title').text_content();C=extract_time_from_breakout_window_title(G)
		if C=='0':E.value='Breakouts are running indefinitely. Starting Timer...';A.open=_A
	else:C='0';E.value='Breakouts are not open. Starting Timer...';A.open=_A
	page.update();print(B);return C
async def web_broadcastTextToBreakouts(page,content):
	A='\n    (content) => {\n        return new Promise((resolve, reject) => {\n            ZoomMtg.broadcast({\n                content: content,\n                success: function(res) {\n                    resolve(res);\n                },\n                error: function(error) {\n                    reject(error);\n                }\n            });\n        });\n    }\n    '
	try:B=await page.evaluate(A,content);return B
	except Exception as C:print(f"Error broadcasting content: {str(C)}");return
def find_participantID(display_name,participant_list):
	for A in participant_list:
		if A[_G]==display_name:return str(A['participantId'])
async def web_allow_unmuting(page):
	A=page
	try:
		await A.get_by_label(_D).evaluate(_B);await A.get_by_label(_Q).evaluate(_B);await A.locator(_R).click()
		if await A.get_by_label(_S).is_visible():print('Already allowed unmuting')
		else:await A.get_by_label(_T).evaluate(_B)
		await A.get_by_role(_C,name=_F).click()
	except Exception:print(_U)
async def web_disallow_unmuting(page):
	A=page
	try:
		await A.get_by_label(_D).evaluate(_B);await A.get_by_label(_Q).evaluate(_B);await A.locator(_R).click()
		if await A.get_by_label(_T).is_visible():print('Already disallowed unmuting')
		else:await A.get_by_label(_S).evaluate(_B)
		await A.get_by_role(_C,name=_F).click()
	except Exception:print(_U)
async def setup_active_speaker_spotlight(page):A=page;await A.evaluate('\n        ZoomMtg.inMeetingServiceListener("onActiveSpeaker", function (data) {\n            const spotlightActiveSpeaker = localStorage.getItem("spotlight_active_speaker");\n            if (spotlightActiveSpeaker !== null) {\n                data.forEach((speaker) => {\n                    ZoomMtg.operateSpotlight({ operate: "add", userId: speaker.userId });\n                    window.pyWebDisallowUnmuting();\n                    console.log(`Spotlight added for user: ${speaker.userName}`);\n                });\n                \n                localStorage.removeItem("spotlight_active_speaker")\n            } else {\n                console.log("No settings found in local storage.");\n            }\n        });\n    ');await A.expose_function('pyWebDisallowUnmuting',lambda:asyncio.create_task(web_disallow_unmuting(A)));print('Active speaker spotlight monitoring started.')
async def trigger_listening_spotlight_active_speaker(page):
	A=page;print('spotlight_active_speaker');await A.evaluate("token => localStorage.setItem('spotlight_active_speaker', token)");await web_allow_unmuting(A);await asyncio.sleep(30);await web_disallow_unmuting(A)
	try:await A.evaluate('removeItem("spotlight_active_speaker")');print('stopped spotlighting active speaker')
	except Exception:print('already stopped')
async def wait_and_spotlight_participant(webSDK_page):
	C='name';B=webSDK_page
	try:
		async with B.expect_event('participantJoined',timeout=15000)as D:print('Waiting for a new participant to join...');A=await D.value
		print(f"New participant joined: {A[C]}");await B.evaluate(f"""
            ZoomMtg.operateSpotlight({{
                operate: 'add',
                userId: '{A["id"]}'
            }});
        """);print(f"Spotlighted participant: {A[C]}")
	except asyncio.TimeoutError:print('No new participant joined within 15 seconds. Ending function.')
def filter_participant_list(original_list):
	E='muted';D='isCoHost';C='participantUUID';B=[]
	for A in original_list:F={_G:A[_G],C:A[C],D:A[D],E:A[E]};B.append(F)
	return B
async def create_test_participants():
	A=await async_playwright().start();B=await A.chromium.launch(headless=_A,args=[_L]);C=await B.new_context(viewport={'width':420,_M:680},locale='en-US',permissions=[])
	for E in range(5):D=await C.new_page();await D.goto(os.path.abspath('WebSDK\\index_component.html'))
	await asyncio.sleep(1000);await A.stop()
if __name__=='__main__':
	async def test():A=await TEST_start_web_module();C=await web_allow_unmuting(A);create_test_participants();await asyncio.sleep(10);B=await web_getBreakoutRooms(A);print(B['unassigned'])
	import asyncio;asyncio.run(test())