import requests
import time
import os

# 上传图片
def upload_image(token, image_path, purpose="vidu", vip=False):
    url = "https://api.chatfire.cn/v1/files"
    headers = {
        'Authorization': f'Bearer {token}',
    }
    files = {
        'file': open(image_path, 'rb'),
        'purpose': (None, purpose)
    }
    params = {
        'vip': str(vip).lower()
    }
    response = requests.post(url, headers=headers, files=files, params=params)
    
    if response.status_code == 200:
        print("图片上传成功")
        return response.json()  # 返回响应内容，包括图片的 URL
    else:
        print(f"图片上传失败，状态码: {response.status_code}, 错误信息: {response.text}")
        return None

# 创建图生视频任务
def create_img_to_video_task(token, prompt, style, aspect_ratio, duration, image_url):
    url = "https://api.chatfire.cn/tasks/vidu?vip=true"
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    payload = {
        "prompt": prompt,
        "style": style,
        "aspect_ratio": aspect_ratio,
        "duration": duration,
        "url": image_url
    }
    response = requests.post(url, json=payload, headers=headers)
    
    if response.status_code == 200:
        print("图生视频任务创建成功")
        return response.json()  # 返回任务ID
    else:
        print(f"图生视频任务创建失败，状态码: {response.status_code}, 错误信息: {response.text}")
        return None

# 获取任务状态
def get_task_status(token, task_id):
    url = f"https://api.chatfire.cn/tasks/{task_id}"
    headers = {
        'Authorization': f'Bearer {token}',
    }
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f"获取任务状态失败，状态码: {response.status_code}, 错误信息: {response.text}")
        return None

# 下载视频
def download_video(video_url, save_path):
    response = requests.get(video_url)
    if response.status_code == 200:
        with open(save_path, 'wb') as file:
            file.write(response.content)
        print(f"视频下载成功: {save_path}")
    else:
        print(f"视频下载失败，状态码: {response.status_code}, 错误信息: {response.text}")

# 主流程：图片上传 -> 图生视频 -> 获取任务状态并下载视频
def process_image_to_video(token, image_path, prompts, style, aspect_ratio, duration, save_video_path):
    # Step 1: 上传图片
    upload_result = upload_image(token, image_path)
    if not upload_result:
        return

    image_url = upload_result.get('url')
    if not image_url:
        print("未能获取到图片URL")
        return

    # Step 2: 遍历所有 prompt 并为每个 prompt 创建图生视频任务
    for i, prompt in enumerate(prompts):
        print(f"\n开始处理第 {i+1} 个任务: {prompt}\n")
        
        video_task = create_img_to_video_task(token, prompt, style, aspect_ratio, duration, image_url)
        if not video_task:
            continue

        task_id = video_task.get('id')
        if not task_id:
            print("未能获取到任务ID")
            continue

        # Step 3: 轮询获取任务状态
        print(f"任务 {task_id} 创建成功，正在等待视频生成...")
    
        while True:
            try:
                task_status = get_task_status(token, task_id)
                if not task_status:
                    break
                
                state = task_status.get('state')
                if state == 'success':
                    print("视频生成成功")
                    video_url = task_status['creations'][0]['uri']  # 获取生成的视频URL
                    # 下载视频
                    download_video(video_url, f"{save_video_path}_{i+1}.mp4")
                    break
                elif state == 'failed':
                    print("视频生成失败")
                    break
                else:
                    print(f"当前任务状态: {state}，继续等待...")
                
                time.sleep(5)  # 每5秒检查一次状态
            
            except requests.exceptions.ConnectionError:
                print("远程主机强行关闭连接，重新尝试...")
                time.sleep(5)  # 等待5秒后重新尝试
            except requests.exceptions.RequestException as e:
                print(f"发生错误: {e}")
                break

# 示例调用
API_key = "sk-oEDQTphWyIXesuau947f40Cd7dE34692B685C92a1056651c"
image_path = "E:\\Pet_AI_Empower\\voive\\dog_dataset\\bg.jpg"
style = "general"
aspect_ratio = "16:9"
duration = 4
save_video_path = "bg_prompt_copy"  # 不带扩展名，以便区分不同视频

# 描述词
prompts = [
    #"乖巧地坐在地上",11111111111111
    #"静静地将后腿折叠在身体下",
    #"优雅地坐在主人的面前",
    #"低头，后腿自然弯曲",
    #"稳定地坐在草地上",
    
    #"将身体舒展在地面上",
    #"前腿伸直，后腿弯曲",
    #"头轻轻地靠在爪子上",
    #"全身紧贴地面，尾巴微微摆动",
    #"放松地趴在阳光下",11111111111
    
    #"高高跃起，四肢悬空",2
    #"敏捷地从地面弹起",1
    #"空中优雅地弯曲身体",
    #"腾空跳跃，耳朵随着动作摆动",3
    #"轻盈地跳向前方",(有点像跑的)
    
    #"前爪伸出，轻触主人的手",
    #"举起前腿，稳稳地与主人握手",1
    #"用前爪轻轻地按住主人的手掌",
    #"抬起一只前爪，期待主人的回应",
    #"友好地将爪子放在主人的手中",
    
    #"狗狗完全趴在地上，前爪伸展，头部贴近地面。它先抬起头，前爪用力，将上半身慢慢撑离地面，后腿逐渐发力抬起身体，最后狗狗完全站立起来，姿势稳固。",
    #"狗狗从完全趴下的状态开始，先是抬起头部，前爪用力将上半身撑起，随后后腿发力，缓慢站起来，最后身体直立，站稳在原地。",#坐下的状态
    #"狗狗趴在地上，前爪向前撑，身体前半部分抬离地面，后腿紧跟着抬起，狗狗的身体逐渐离开地面，慢慢站直，最后完全站立起来。",
    #"狗狗趴在地面上，头部靠近地面。它先用前爪撑地，抬起上半身，接着后腿用力将身体从地面抬起，狗狗慢慢从趴下状态站起来，最终直立。",
    #"狗狗趴在地上，前爪和后腿伸展。它先抬起头，前爪用力将上身推起，然后后腿逐步用力，整个身体从地面站起，最终站得笔直，姿势稳定。",    #有趴下状态，但是站立动作不自然
    #"狗狗安静地趴在地上，先抬头并用前爪撑起前身，后腿慢慢从地面上抬起，身体逐渐直立，最后完全站立，动作流畅自然。",
    #"狗狗趴在地上，前爪开始用力撑起上身，后腿随后发力，整个身体从地面抬起，最后站直在原地，狗狗姿态平稳。",
    
    
    #"期待地举起前爪，进行握手动作",  #32
    #"稳定地将爪子放在主人的手上，表现出亲密",
    #"轻轻用爪子拍打主人的手，显示友善",    
    #"从坐着的姿势中抬起前腿，慢慢站起" ,
    #"逐渐从坐下的位置转变为站立，展现活力" ,
    #"从趴下的姿势中抬起前爪，身体向上站起" ,
    #"缓缓起身，从舒展的趴姿转为稳健的站立" ,#38
    
    #"友好地抬起前爪，轻轻搭在主人的手上，展现亲昵",#39
    #"将前腿伸出，主动与主人握手，表达亲密互动",
    #"稳定地用爪子轻触主人的手，显示出信任和依赖",
    #"期待地抬起前爪，与主人手心相贴，完成握手",
    #"俏皮地用前爪拍打主人的手，展示出活泼和友好",
    #"从坐着的姿势中，前爪先抬起，优雅地转为站立",
    #"从趴下的姿势中，先抬起头，然后用前腿支撑身体起立",
    #"缓缓起身，前腿稳稳地撑起，尾巴高高翘起，显示自信",#失败了    #下面这个好
    #"狗坐在主人面前，耳朵竖起，目光专注。它抬起一只前爪，轻轻搭在主人的手掌上，仿佛在说“你好！”狗狗的表情愉悦，尾巴微微摇摆，展示出亲密和友好。主人微笑着回应，轻轻握住狗狗的爪子，彼此的互动让这一刻充满温馨。",
    #下面这条趴下
    #"狗狗舒适地趴在地上，前爪自然地伸展，耳朵柔软地垂下，显得十分放松。随着主人温柔的召唤声，狗狗的耳朵迅速竖起，眼睛睁大，流露出兴奋与期待。它开始先抬起一只前爪，慢慢地将爪子推向地面，准备支撑起身体。接着，狗狗微微弓起背部，后腿用力，前腿也随之向下用力，身体向上倾斜。尾巴高高翘起，像个小旗子一样摇摆，展现出它的活力与兴奋。最后，狗狗的前腿稳稳落在地面上，后腿支撑起整个身体，缓缓站直，目光坚定地注视着主人，似乎在说：“我准备好迎接新的一天了！"
    ####"狗狗懒洋洋地趴在地上，前爪轻轻伸展，耳朵垂下，显得十分放松。听到主人的召唤声，狗狗的耳朵瞬间竖起，眼中闪烁着兴奋的光芒。它先将一只前爪缓缓抬起，轻触地面，随后用力撑起前身，背部微微弓起。狗狗的后腿开始紧绷，随着身体的倾斜，它开始努力地将后腿推开，慢慢向上站起。尾巴兴奋地摇摆，仿佛在为这个动作加油。最后，狗狗稳稳地站起来，目光直视前方，身体挺直，充满活力，像是在迎接新的冒险。",
    #"狗狗懒洋洋地趴在地上，前爪自然放松，耳朵垂下，显得十分惬意。随着主人柔和的召唤声，狗狗的耳朵立刻竖起，眼中闪现出兴奋的光芒。它缓缓抬起一只前爪，轻轻按在地面上，随后用力撑起身体，背部微微弓起，显示出努力的样子。后腿开始用力，稳稳地推开地面，逐渐站起。狗狗的尾巴高高翘起，兴奋地摇摆着，传达出它的快乐与期待。当它完全站起来时，四肢稳稳地落在地面上，身体挺直，目光坚定地注视着主人，似乎在说：“我准备好了，随时出发！”这一刻，狗狗散发出满满的自信与活力，整个过程流畅自然，没有任何浮动的感觉。"
    #"狗狗舒适地趴在地上，前爪自然放松，耳朵轻轻垂下，显得惬意而放松。听到主人的召唤，狗狗的耳朵瞬间竖起，眼中闪烁着兴奋的光芒。它首先微微抬起头，接着一只前爪慢慢按在地面上，准备支撑身体。然后，狗狗用力推开地面，缓缓弓起背部，开始站立。后腿紧绷，逐渐将身体完全支撑起来，尾巴兴奋地摇摆，仿佛在为这一动作欢呼。站立时，狗狗目光坚定，向前注视，散发出自信的气息。此时，它的前爪轻轻搭在主人伸出的手上，展现出亲密的互动，似乎在请求主人给予鼓励和赞赏。",
    #"趴下后坐起来"

    #"A standing dog gradually sits down, moving naturally with a smooth transition.",
    "一只站着的狗逐渐坐下，动作自然，过渡流畅",
    
    #"The dog sits quietly in front of its owner, with a gentle look in its eyes.",
    "狗狗安静地坐在主人面前，眼神温柔。",
    
    #"Sitting obediently on the ground.",
    "乖巧地坐在地上",
    
    #"A dog slowly lies down on the ground, first bending its front legs as its body lowers closer to the ground, front paws gently stretched out, then its back legs follow, lying flat. Finally, it lowers its head and fully relaxes, lying peacefully.",
    "一只狗在地上慢慢趴下，先是弯曲前腿，身体逐渐贴近地面，前爪轻轻伸展，然后后腿也跟着平铺在地上，头部放低，最后完全放松地趴在地上。",
    
    #"Starting from a lying position, the dog pushes itself up with its front paws, slowly lifting its back legs, gracefully rising to stand with steady posture.c",
    "狗狗从趴着姿势开始，前爪用力撑起身体，后腿慢慢抬起，狗狗缓缓站立起来，姿势优雅且稳固。",
    
    #"Relaxing in the sunlight, lying peacefully",
    "放松地趴在阳光下",
    
    #"The dog springs up from the ground with agility, all four legs in the air.",
    "狗狗敏捷地从地面弹起，四肢悬空。",
    
    #"Quickly springing up from the ground.",
    "敏捷地从地面弹起",
    
    #"Leaping high into the air, all four paws off the ground.",
    "高高跃起，四肢悬空",
    
    #"The dog places its paw gently in its owner's hand in a friendly gesture.",
    "友好地将爪子放在主人的手中",
    
    #"Raising its front leg, the dog firmly shakes hands with its owner.",
    "举起前腿，稳稳地与主人握手",
    
    #"The dog sits in front of its owner, ears perked up and eyes focused. It lifts a front paw and gently places it on the owner’s hand, as if saying ‘hello!’ The dog’s expression is happy, and its tail wags slightly, showing affection and friendliness. The owner smiles back and lightly grips the dog’s paw, making the moment warm and full of connection.",
    "狗坐在主人面前，耳朵竖起，目光专注。它抬起一只前爪，轻轻搭在主人的手掌上，仿佛在说“你好！”狗狗的表情愉悦，尾巴微微摇摆，展示出亲密和友好。主人微笑着回应，轻轻握住狗狗的爪子，彼此的互动让这一刻充满温馨。",
    
    #"The dog, lying down, pushes up with its front legs, then gradually uses its back legs to lift its whole body, slowly transitioning from lying to standing, ears perking up slightly.",#"狗狗趴着，先用前腿撑起身体，后腿逐步发力将整个身体抬起，狗狗慢慢从趴姿变为站立状态，耳朵微微竖起。",
    "狗躺下后，用前腿将身体撑起，然后逐渐用后腿将整个身体抬起，慢慢地从躺着过渡到站着，耳朵微微竖起。",        
    
    #"The dog lies lazily on the ground, front paws gently stretched out, ears drooping, looking completely relaxed. As soon as it hears its owner’s call, its ears perk up instantly, and excitement lights up its eyes. It slowly lifts one front paw, lightly touching the ground, then pushes up with effort, arching its back slightly. Its hind legs tense as its body leans forward, and it begins to push off with its back legs, slowly rising to a stand. Its tail wags excitedly, almost cheering itself on. Finally, the dog stands firmly, eyes focused ahead, body straight and full of energy, as if ready to embrace a new adventure.",
    "狗狗懒洋洋地趴在地上，前爪轻轻伸展，耳朵垂下，显得十分放松。听到主人的召唤声，狗狗的耳朵瞬间竖起，眼中闪烁着兴奋的光芒。它先将一只前爪缓缓抬起，轻触地面，随后用力撑起前身，背部微微弓起。狗狗的后腿开始紧绷，随着身体的倾斜，它开始努力地将后腿推开，慢慢向上站起。尾巴兴奋地摇摆，仿佛在为这个动作加油。最后，狗狗稳稳地站起来，目光直视前方，身体挺直，充满活力，像是在迎接新的冒险。",        
    
    #00000000000
    
    #"一只活力满满的狗狗轻快地跳起，四肢离地，耳朵随动作飘动，脸上带着兴奋的神情。",
    #"A lively dog jumps gracefully into the air, all four legs off the ground, ears flapping with the motion, and an excited expression on its face.",  
    #"A lively dog leaps into the air, all four paws off the ground, ears flapping with the movement, and an excited expression on its face.",            #111111111
    #"这只黑白边牧优雅地趴在地上，前肢伸直，头微微低垂，目光专注地注视着前方，等待主人指令。",
    #"The dog elegantly lies down on the ground, front legs stretched out, head slightly lowered, and its eyes focused intently ahead, waiting for a command.",
    #"The dog gracefully lies down, front legs stretched out, head slightly lowered, and eyes focused intently ahead, waiting for its owner’s command.",   #00000000000
    #"狗狗用后腿站立，前爪轻轻抬起，身体平衡，眼睛闪烁着对周围环境的好奇。",
    #"The dog up on its hind legs, front paws raised slightly, maintaining balance, with eyes gleaming in curiosity as it surveys its surroundings.",
    #"狗狗坐着，伸出一只前爪与主人握手，尾巴轻轻摇摆，表现出友好与信任。",
    #"The dog sits and extends one of its front paws to shake hands with its owner, tail wagging gently, showing friendliness and trust.",
    #"The dog sits and extends a paw to shake hands with its owner, tail gently wagging, showing friendliness and trust.",                     #00000000000
    #"狗狗端坐在草地上，背部挺直，目光温和，神态安详，偶尔抬头看向远处。",
    #"The dog sits upright on the grass, back straight, eyes calm and gentle, occasionally glancing into the distance with a peaceful demeanor."
    #"The dog sits upright on the grass, back straight, with a calm and gentle gaze. It occasionally looks up into the distance, appearing peaceful and serene."   #
    
]

# 执行主流程
process_image_to_video(API_key, image_path, prompts, style, aspect_ratio, duration, save_video_path)
