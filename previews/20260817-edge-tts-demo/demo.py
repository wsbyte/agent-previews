import asyncio
import os
import edge_tts

DEMO_DIR = "/Users/mikon/.gemini/antigravity/scratch/edge_tts_demo"

async def generate_speech(text: str, voice: str, output_audio: str, output_sub: str = None, rate: str = "+0%", pitch: str = "+0Hz"):
    """
    使用 edge-tts 生成高品质语音及字幕
    :param text: 需要朗读的文本
    :param voice: 音色名称（如 zh-CN-YunxiNeural）
    :param output_audio: 音频保存路径 (.mp3)
    :param output_sub: 字幕保存路径 (.srt) 可选
    :param rate: 语速调整（如 "+10%" 或 "-10%"）
    :param pitch: 音调调整（如 "+5Hz" 或 "-5Hz"）
    """
    print(f"🎙️ 正在生成: [{voice}] ...")
    communicate = edge_tts.Communicate(text=text, voice=voice, rate=rate, pitch=pitch)
    
    if output_sub:
        sub_maker = edge_tts.SubMaker()
        with open(output_audio, "wb") as audio_file:
            async for chunk in communicate.stream():
                if chunk["type"] == "audio":
                    audio_file.write(chunk["data"])
                elif chunk["type"] in ("WordBoundary", "SentenceBoundary"):
                    sub_maker.feed(chunk)
                    
        with open(output_sub, "w", encoding="utf-8") as sub_file:
            sub_file.write(sub_maker.get_srt())
        print(f"   ✅ 音频已保存: {os.path.basename(output_audio)} ({os.path.getsize(output_audio):,} 字节)")
        print(f"   ✅ 字幕已保存: {os.path.basename(output_sub)}")
    else:
        await communicate.save(output_audio)
        print(f"   ✅ 音频已保存: {os.path.basename(output_audio)} ({os.path.getsize(output_audio):,} 字节)")

async def main():
    os.makedirs(DEMO_DIR, exist_ok=True)
    print("========================================")
    print("🚀 Edge-TTS 自动化配音生成示例启动")
    print("========================================\n")

    # 示例 1：经典短视频/影视解说男声（云希）+ 生成 SRT 格式字幕
    text_yunxi = "注意看，眼前这个男人叫小帅，他正在用 edge-tts 自动生成短视频配音和字幕。"
    audio_yunxi = os.path.join(DEMO_DIR, "demo_yunxi_解说男声.mp3")
    sub_yunxi = os.path.join(DEMO_DIR, "demo_yunxi_解说男声.srt")
    await generate_speech(text=text_yunxi, voice="zh-CN-YunxiNeural", output_audio=audio_yunxi, output_sub=sub_yunxi, rate="+10%")

    # 示例 2：自然温和播音女声（晓晓）
    text_xiaoxiao = "欢迎使用 edge-tts 语音合成系统。无需安装浏览器，无需专业显卡，即可快速批量生成自然流畅的语音。"
    audio_xiaoxiao = os.path.join(DEMO_DIR, "demo_xiaoxiao_温柔女声.mp3")
    await generate_speech(text=text_xiaoxiao, voice="zh-CN-XiaoxiaoNeural", output_audio=audio_xiaoxiao)

    # 示例 3：陕西方言 / 特色音色（陕西晓妮）
    text_shaanxi = "兄弟们，今儿个咱们聊一聊这个配音自动化，确实是省心又方便得很！"
    audio_shaanxi = os.path.join(DEMO_DIR, "demo_shaanxi_方言特色.mp3")
    await generate_speech(text=text_shaanxi, voice="zh-CN-shaanxi-XiaoniNeural", output_audio=audio_shaanxi)

    print("\n========================================")
    print("🎉 所有示例音频及字幕已全部成功生成！")
    print(f"📁 文件存储目录: {DEMO_DIR}")
    print("========================================")

if __name__ == "__main__":
    asyncio.run(main())
