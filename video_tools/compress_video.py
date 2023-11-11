import os
import subprocess
from multiprocessing import Pool
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))
from log.logger import logger

def compress_single_video(args):
    input_path, output_path, crf_value, use_gpu = args

    if use_gpu:
        command = ['ffmpeg', '-i', input_path, '-c:v', 'h264_nvenc', '-preset', 'medium', '-crf', crf_value, output_path]
    else:
        command = ['ffmpeg', '-i', input_path, '-vcodec', 'libx264', '-crf', crf_value, output_path]

    try:
        subprocess.run(command, check=True)
        logger.info(f"Compressed {input_path} successfully.")
        return (input_path, "Success")
    except subprocess.CalledProcessError:
        logger.info(f"Failed to compress {input_path}.")
        return (input_path, "Failed")

def compress_video(input_folder, output_folder, compression_ratio, processes=4, use_gpu=True):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    tasks = []

    for root, dirs, files in os.walk(input_folder):
        for file in files:
            if file.lower().endswith(('.mp4', '.mkv', '.avi', '.flv', '.mov')):
                input_path = os.path.join(root, file)
                relative_path = os.path.relpath(root, input_folder)
                output_path_directory = os.path.join(output_folder, relative_path)

                if not os.path.exists(output_path_directory):
                    os.makedirs(output_path_directory)

                output_path = os.path.join(output_path_directory, file)
                crf_value = str(18 + (10 * compression_ratio))
                
                tasks.append((input_path, output_path, crf_value, use_gpu))

    with Pool(processes) as pool:
        results = pool.map(compress_single_video, tasks)

    return results

if __name__ == "__main__":
    # 输入和输出的文件夹路径
    folders = ['G:\\gopro\\have']
    output_folder = 'F:\\video_output'  # 输出文件夹
    
    # 压缩比率（0.0到1.0之间，0表示几乎无损，1表示高度压缩）
    compression_ratio = 0.5  # 可以根据需要调整这个值

    processes = 4  # 并行处理的进程数

    use_gpu = True  # 是否使用GPU进行压缩
    
    for folder in folders:
        results = compress_video(folder, output_folder, compression_ratio, processes)
        for result in results:
            logger.info(f"folder:{folder}: {result[0]}: {result[1]}")
