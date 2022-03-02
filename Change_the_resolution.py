import os
import time
import tkinter.ttk as ttk
import tkinter.messagebox as msgbox
from tkinter import *
from tkinter import filedialog
from PIL import Image

#리소스 파일 주소를 연결시켜서 이미지 불러오기
def resource_path(relative_path):          
    try:
        base_path = sys._MEIPASS 
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

root = Tk()
# 아이콘 이미지를 불러올때 resource_path 사용 ("위치/파일이름")
root.iconbitmap(resource_path("gui_program/moniter.ico")) 
root.title("해상도 변경 프로그램")
root.configure(bg='green')



# 파일 추가
def add_file():
    files = filedialog.askopenfilenames(title="해상도를 변경할 이미지를 선택하세요", filetypes=(("이미지 파일", "*.png, *.jpg"), ("모든 파일", "*.*")),\
        initialdir=r"C:\Users") # 최초경로설정

    #선택한 파일목록
    for file in files:
        list_file.insert(END, file)

# 파일 삭제
def del_file():
    #print(list_file.curselection())
    for index in reversed(list_file.curselection()):
        list_file.delete(index)

# 저장 경로
def browse_dest_path():
    folder_selected = filedialog.askdirectory()
    if folder_selected == '':
        print("폴더 선택 취소")
        return
    #print(folder_selected)
    txt_dest_path.delete(0, END)
    txt_dest_path.insert(0, folder_selected)

# 이미지 업데이트
def update_image():
    try:
        # 가로 넓이
        img_width =cmb_width.get()
        if img_width == "원본유지":
            img_width = -1 # -1 일때는 원본 기준으로 통합하라
        else:
            img_width = int(img_width)

        images = [Image.open(x) for x in list_file.get(0, END)]

        # 포맷
        img_format = cmb_format.get().lower() 

        # 이미지 사이즈 리스트에 넣어서 하나씩 처리
        image_sizes = [] 

        if img_width > -1: #width 값 변경
            image_sizes = [(int(img_width), int(img_width * x.size[1] / x.size[0])) for x in images]

        else: # 원본 사이즈 사용
            image_sizes = [(x.size[0], x.size[1]) for x in images]    

        widths, heights = zip(*(image_sizes))

        # 최대 넓이, 전체 높이 구해옴
        max_width, total_height = max(widths), sum(heights)

        # 스케치북 준비
        result_img = Image.new("RGB", (max_width, total_height), (255, 255, 255))
        y_offset = 0 # y 위치

        for idx, img in enumerate(images):
                if img_width > -1:
                    img = img.resize(image_sizes[idx])

                result_img.paste(img, (0, y_offset))
                y_offset += (img.size[1])

                progress = (idx + 1) / len(images) * 100
                p_var.set(progress)
                progress_bar.update()
        
        curr_time = time.strftime("%Y_%m_%d_%H%M%S")
        file_name = (("{}_photo.").format(curr_time) + img_format)
        dest_path = os.path.join(txt_dest_path.get(), file_name)
        result_img.save(dest_path)
        msgbox.showinfo("알림", "완료되었습니다.")
    except Exception as err: # 예외처리
        msgbox.showerror("에러", err)

# 시작
def start():
    # 파일 목록 확인
    if list_file.size() == 0:
        msgbox.showwarning("경고", "이미지 파일을 추가하세요")
        return

    # 저장 경로 확인
    if len(txt_dest_path.get()) == 0:
        msgbox.showwarning("경고", "저장 경로를 선택하세요")
        return
    
    # 이미지 통합 작업
    update_image()



# 저장 경로 프레임
path_frame = LabelFrame(root, bg= 'green', fg='white', text="저장경로", font=("None", 11))
path_frame.pack(fill="x", padx=5, pady=5, ipady=5)

txt_dest_path = Entry(path_frame)
txt_dest_path.pack(side="left", fill="x", expand=True, padx=5, pady=5, ipady=4) #ipad 높이변경

btn_dest_path = Button(path_frame, bg= 'darkgreen', fg='white', text="경로설정",font=("None", 10), width=10, command=browse_dest_path)
btn_dest_path.pack(side="right", padx=5, pady=5)

# 리스트 프레임
list_frame = LabelFrame(root, bg= 'green', fg='white', text="[해상도 변경할 파일을 추가하세요]", font=("None", 11))
list_frame.pack(fill="both", padx=5, pady=5)

scrollbar = Scrollbar(list_frame)
scrollbar.pack(side="right", fill="y")

list_file =Listbox(list_frame, selectmode="extended", height=2, yscrollcommand=scrollbar.set)
list_file.pack(side="left", fill="both", expand=True)
scrollbar.config(command=list_file.yview)

# 파일 프레임 (파일 추가, 선택 삭제)
file_frame = Frame(root, bg= 'green')
file_frame.pack(fill="x", padx=5, pady=3)

# 추가/삭제 버튼
btn_add_file = Button(file_frame, bg= 'darkgreen', fg='white', padx=3, pady=3, width=7, text="파일추가",font=("None", 10), command=add_file)
btn_add_file.pack(side="right")

btn_del_file = Button(file_frame, bg= 'darkgreen', fg='white', padx=3, pady=3, width=7, text="선택삭제",font=("None", 10), command=del_file)
btn_del_file.pack(side="right")

# 옵션 프레임
frame_option = LabelFrame(root,  bg= 'green', fg='white',  text="옵션", font=("None", 11))
frame_option.pack(padx=5, pady=5, ipady=5)

# 가로 넓이 레이블
lbl_width = Label(frame_option, bg= 'darkgreen', fg='white',  text="해상도", width=8)
lbl_width.pack(side="left", padx=5, pady=5)

# 가로 넓이 콤보박스
opt_width = ["1920", "2560", "3840", "7680"]
cmb_width = ttk.Combobox(frame_option, state="readonly", values=opt_width, width=10)
cmb_width.current(0)
cmb_width.pack(side="left", padx=5, pady=5)

# 파일 포맷 옵션 레이블
lbl_format = Label(frame_option, bg= 'darkgreen', fg='white', text="포맷", width=8)
lbl_format.pack(side="left", padx=5, pady=5)

# 파일 포맷 옵션 콤보박스
opt_format = ["JPG", "PNG", "BMP"]
cmb_format = ttk.Combobox(frame_option, state="readonly", values=opt_format, width=10)
cmb_format.current(0)
cmb_format.pack(side="left", padx=5, pady=5)

# 진행 상황 Progress Bar
frame_progress = LabelFrame(root, bg= 'green', fg='white', text="완료", font=("None", 11))
frame_progress.pack(fill="x", padx=5, pady=5, ipady=5)

p_var = DoubleVar()
progress_bar = ttk.Progressbar(frame_progress, maximum=100, variable=p_var)
progress_bar.pack(fill="x", padx=5, pady=5)

# 실행 프레임
frame_run = Frame(root, bg= 'green')
frame_run.pack(fill="x", padx=8, pady=8)

# 닫기 버튼 / 시작 버튼
btn_close = Button(frame_run, bg= 'darkgreen', fg='white', padx=3, pady=3, text="닫기",font=("None", 10), width=8, command=root.quit)
btn_close.pack(side="left", padx=3, pady=3)

btn_start = Button(frame_run, bg= 'darkgreen', fg='white', padx=3, pady=3, text="시작",font=("None", 10), width=8, command=start)
btn_start.pack(side="right", padx=3, pady=3)

root.resizable(False, False)
root.mainloop()
