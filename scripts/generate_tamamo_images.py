#!/usr/bin/env python3
"""
玉藻前文章配图生成脚本 - M1 8GB 优化版
使用 Stable Diffusion 1.5 + 优化设置，适应低内存环境
"""

import torch
import os
from diffusers import StableDiffusionPipeline
import time

# 为玉藻前文章18个小节准备的提示词
PROMPTS = [
    # 一节：妖狐的三国流转
    ("1.1_印度华阳天", "Ancient Indian palace, beautiful fox spirit disguised as court lady Huayangtian, golden robes, nine tails visible in shadow, Indian architecture, mysterious atmosphere, high quality, detailed"),
    ("1.2_中国妲己", "Chinese Shang dynasty palace, stunning concubine Daji, silk robes, nine fox tails visible in shadow, bronze vessels, oracle bones, ancient China, detailed painting"),
    ("1.3_日本玉藻前", "Japanese Heian period court, beautiful Tamamo-no-Mae in elegant kimono, entering palace, traditional architecture, cherry blossoms, ukiyo-e style"),
    
    # 二节：宫廷中的妖狐魅影
    ("2.1_入宫得宠", "Tamamo-no-Mae playing koto, Heian court ladies admiring her, palace interior, golden screens, traditional Japanese painting"),
    ("2.2_天皇病重", "Sick Emperor Toba in bed, dark palace room, mysterious aura, fox shadow on wall, traditional Japanese painting style"),
    ("2.3_阴阳师怀疑", "Yin-Yang master Abe Yasunari meditating, seeing nine-tailed fox shadow, moonlight, Edo period style, mysterious"),
    
    # 三节：真身败露与逃亡
    ("3.1_识破妖身", "Yin-Yang masters casting spells, nine-tailed fox spirit revealed, magical circles, Japanese mythology, dramatic scene"),
    ("3.2_天皇的震惊", "Emperor Toba shocked expression, mirror reflection showing fox ears, palace room, dramatic lighting, ukiyo-e style"),
    ("3.3_那须野的藏身", "Abandoned mansion in Nasu field, moonlight, mysterious atmosphere, Japanese countryside, traditional painting"),
    
    # 四节：那须野的讨伐之战
    ("4.1_三浦介与上总介", "Japanese samurai warriors preparing for battle, traditional armor, Nasu field background, ukiyo-e style"),
    ("4.2_激战那须野", "Epic battle, nine-tailed fox spirit giant form, samurai warriors fighting, dynamic action, Japanese mythology"),
    ("4.3_妖狐之死", "Nine-tailed fox falling, arrow in forehead, dramatic sunset, Japanese painting style, tragic scene"),
    
    # 五节：杀生石的诅咒
    ("5.1_石头诞生", "Giant stone formation, poisonous aura, dead vegetation, Japanese landscape, mysterious atmosphere"),
    ("5.2_镇魂与封印", "Buddhist monk chanting sutra, glowing stone, peaceful atmosphere, Japanese temple, religious art"),
    ("5.3_现代遗迹", "Tourists visiting Sessho-seki stone, modern Japan, historical site, realistic photo style"),
    
    # 六节：文化影响与后世演绎
    ("6.1_文学与戏剧", "Traditional Japanese theater, Noh mask, scroll paintings, Tamamo-no-Mae story, classical art"),
    ("6.2_现代流行文化", "Anime style Tamamo-no-Mae, modern illustration, vibrant colors, manga aesthetic"),
    ("6.3_东亚妖狐文化的交融", "Three women representing India China Japan, fox spirits, cultural exchange, artistic composition"),
]

def setup_pipeline():
    """设置优化后的pipeline，适应M1 8GB内存"""
    print("正在加载模型（首次运行需要下载约4GB）...")
    
    # 使用 SD 1.5，更适合低内存
    model_id = "runwayml/stable-diffusion-v1-5"
    
    # M1 使用 MPS 后端，float16 节省内存
    pipe = StableDiffusionPipeline.from_pretrained(
        model_id,
        torch_dtype=torch.float16,
        use_safetensors=True,
    )
    
    # 启用内存优化
    pipe = pipe.to("mps")  # M1 的 Metal Performance Shaders
    pipe.enable_attention_slicing()  # 降低内存峰值
    pipe.enable_xformers_memory_efficient_attention() if hasattr(pipe, 'enable_xformers_memory_efficient_attention') else None
    
    print("模型加载完成！")
    return pipe

def generate_image(pipe, prompt, negative_prompt, output_path, width=512, height=512):
    """生成单张图片"""
    try:
        # 生成图片（降低步数以节省时间和内存）
        with torch.no_grad():
            image = pipe(
                prompt=prompt,
                negative_prompt=negative_prompt,
                width=width,
                height=height,
                num_inference_steps=20,  # 减少步数
                guidance_scale=7.5,
            ).images[0]
        
        # 保存图片
        image.save(output_path)
        return True
    except Exception as e:
        print(f"生成失败: {e}")
        return False

def main():
    # 创建输出目录
    output_dir = "/Users/fanweijun/vanvj0001/content/posts/japan/images/tamamo"
    os.makedirs(output_dir, exist_ok=True)
    
    # 检查内存
    print("注意：M1 8GB 内存运行 SD 1.5 会比较吃力")
    print("建议：关闭其他应用，留出足够内存")
    print("生成每张图约需 2-5 分钟\n")
    
    # 设置 pipeline
    pipe = setup_pipeline()
    
    # 通用负面提示词
    negative_prompt = "low quality, blurry, distorted, ugly, bad anatomy, watermark, signature, text"
    
    # 生成图片（先测试1张）
    print(f"准备生成 {len(PROMPTS)} 张图片...")
    print("注意：为节省内存，使用 512x512 分辨率，之后可放大到 16:9")
    
    # 先只生成第一张测试
    name, prompt = PROMPTS[0]
    output_path = os.path.join(output_dir, f"{name}.png")
    
    print(f"\n测试生成第一张: {name}")
    print(f"提示词: {prompt[:80]}...")
    
    start = time.time()
    if generate_image(pipe, prompt, negative_prompt, output_path):
        elapsed = time.time() - start
        print(f"✓ 生成成功！用时 {elapsed:.1f} 秒")
        print(f"保存至: {output_path}")
    else:
        print("✗ 生成失败")

if __name__ == "__main__":
    main()
