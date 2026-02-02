import requests
import json

# 配置信息
config = {
    "api_url": "https://api.chatfire.cn/v1/chat/completions",
    "api_key": "sk-qQVS13OjKdw0NqYAF490Cf8690C5457eB717F1E4AdC68b3f",
    "video_url": "https://datawin-public.oss-cn-beijing.aliyuncs.com/sxfdl/1.mp4",
    "output_file": "video_analysis_result.txt"
}

def analyze_video(video_url, prompt):
    """使用API分析视频"""
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {config["api_key"]}'
    }
    
    payload = {
        "model": "qwen3-vl-plus-video-thinking",
        "messages": [
            {
                "role": "system",
                "content": """你是一位专业的短剧编剧。请将视频内容转换为剧本格式。"""
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": prompt
                    },
                    {
                        "type": "video_url",
                        "video_url": {
                            "url": video_url
                        }
                    }
                ]
            }
        ]
    }

    try:
        print("正在分析视频...")
        response = requests.post(
            config["api_url"],
            headers=headers,
            json=payload,
            timeout=60
        )
        
        if response.status_code == 200:
            result = response.json()
            return result.get('choices', [{}])[0].get('message', {}).get('content')
        else:
            print(f"错误信息：{response.text}")
            return None
    except Exception as e:
        print(f"分析失败: {e}")
        return None

def main():
    try:
        prompt = """请将这个视频转换为可供表演的剧本格式。"""
        
        print("开始分析视频...")
        analysis_result = analyze_video(config['video_url'], prompt)
        
        if analysis_result:
            with open(config['output_file'], 'w', encoding='utf-8') as output_file:
                output_file.write(analysis_result)
            print(f"\n=== 剧本内容 ===\n")
            print(analysis_result)
            print(f"\n剧本已保存到 {config['output_file']}")
        else:
            print("分析失败，未能生成剧本。")
    except Exception as e:
        print(f"发生错误：{str(e)}")

if __name__ == "__main__":
    main()
