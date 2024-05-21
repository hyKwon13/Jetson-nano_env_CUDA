import cv2
import numpy as np
import time
def process_image_cpu(image):
    # CPU에서 여러 단계의 GaussianBlur를 사용한 이미지 처리
    for _ in range(100): # 10번 반복하여 GaussianBlur 적용
        image = cv2.GaussianBlur(image, (15, 15), 0)
    return image
def process_image_gpu(gpu_blur, gpu_image):
    # GPU에서 여러 단계의 GaussianBlur를 사용한 이미지 처리
    for _ in range(100): # 10번 반복하여 GaussianBlur 적용
        gpu_image = gpu_blur.apply(gpu_image)
    result = gpu_image.download()
    return result
def main():
    # 웹캠에서 이미지 캡처
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("웹캠을 열 수 없습니다.")
        return
    ret, frame = cap.read()
    if not ret:
        print("이미지를 캡처할 수 없습니다.")
        return
    # GPU 초기화
    gpu_image = cv2.cuda_GpuMat()
    gpu_image.upload(frame)
    gpu_blur = cv2.cuda.createGaussianFilter(gpu_image.type(), -1, (15, 15), 0)
    # CPU 처리 시간 측정
    start_time = time.time()
    cpu_result = process_image_cpu(frame.copy())
    cpu_time = time.time() - start_time
    # GPU 처리 시간 측정
    start_time = time.time()
    gpu_result = process_image_gpu(gpu_blur, gpu_image)
    gpu_time = time.time() - start_time
    print(f"CPU 처리 시간: {cpu_time:.4f} 초")
    print(f"GPU 처리 시간: {gpu_time:.4f} 초")
    # 결과 이미지 표시 (원하는 경우)
    cv2.imshow("Original", frame)
    cv2.imshow("CPU Result", cpu_result)
    cv2.imshow("GPU Result", gpu_result)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    cap.release()
if __name__ == "__main__":
    main()
