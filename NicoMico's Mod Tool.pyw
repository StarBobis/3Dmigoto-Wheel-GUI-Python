# -*- coding: gbk -*-
# ����ü�������һ�У���Ϊ���ǵ�3Dmigoto-Wheelʹ�õľ���GBK����,�����޷�������ʾ�����������������

# ����tkinter��صİ�
from tkinter import messagebox
import tkinter as tk
from tkinter import ttk
from tkinter.filedialog import askopenfilename
from tkinter.filedialog import asksaveasfilename
from tkinter import filedialog

# �����Ҫ�İ�
import os
import re
import json
import subprocess

# �����õ��İ�
import threading
import webbrowser
import ctypes
import shutil

# ����3Dmigoto-Wheel.exe����·��
wheel_path = os.getcwd() + '\\NicoMicoModTool\\NicoMicoModTool.exe'
config_json_path = "NicoMicoModTool/Config.json"
wheel_game_type = ""

WheelName = "NicoMico��s Mod Tool V1.1.0.17"
WheelErrorMSG = WheelName + " Error"
WheelInfoMSG = WheelName + " Info"


def hash_format_check(hash_str, check_attribute):
    if hash_str == "":
        messagebox.showinfo("Config Error", check_attribute + "Ϊ�գ�������һ��")
        return False
    if has_chinese(hash_str):
        messagebox.showinfo("Config Error", check_attribute + "���ܳ�������")
        return False

    if len(hash_str) != 8:
        messagebox.showinfo("Config Error", check_attribute + "��hashֵ����, ���ȱ���Ϊ8")
        return False

    return True


def on_closing():
    # �ڴ��ڹر�ʱִ�еĲ���
    exit(0)


def on_select_tangent(event):
    selected_item = combobox_tangent.get()


def has_chinese(text):
    pattern = re.compile(r'[\u4e00-\u9fff]')  # ƥ�������ַ���������ʽ
    return bool(re.search(pattern, text))


def contains_only_digits(text):
    # ʹ��������ʽƥ���ı��Ƿ�ֻ��������
    pattern = r'^\d+$'
    match = re.match(pattern, text)
    return match is not None


def handle_open_output_folder_command():
    path = filedialog.askdirectory()
    if path != "":
        directory_path = path + "/"
        text_box_output_folder.configure(state='normal')
        text_box_output_folder.delete("1.0", "end")
        text_box_output_folder.insert("1.0", directory_path)
        text_box_output_folder.configure(state='disabled')


def handle_open_loader_folder_command():
    path = filedialog.askdirectory()
    if path != "":
        directory_path = path + "/"
        text_box_loader_folder.configure(state='normal')
        text_box_loader_folder.delete("1.0", "end")
        text_box_loader_folder.insert("1.0", directory_path)
        text_box_loader_folder.configure(state='disabled')


def handle_open_fa_folder_command():
    path = filedialog.askdirectory()
    if path != "":
        directory_path = path.split("/")[-1]
        text_box_fa_folder.configure(state='normal')
        text_box_fa_folder.delete("1.0", "end")
        text_box_fa_folder.insert("1.0", directory_path)
        text_box_fa_folder.configure(state='disabled')
    else:
        text_box_fa_folder.configure(state='normal')
        text_box_fa_folder.delete("1.0", "end")
        text_box_fa_folder.insert("1.0", "latest")
        text_box_fa_folder.configure(state='disabled')


def handle_run_command(command):
    try:
        check_config_result = check_and_set_and_save_config()
        if check_config_result:
            output = subprocess.check_output(wheel_path + " " + command, shell=True)
            output = output.decode("gbk")  # ���ֽ�ת��Ϊ�ַ���
            output_text.insert(tk.END, output)
            notebook.select(tab2)  # ��ת���ڶ���ѡ�
            output_text.see(tk.END)  # �������ı���ײ�
            messagebox.showinfo(WheelInfoMSG, "Run " + command + " Successful.")

    except subprocess.CalledProcessError as e:
        output = e.output.decode("gbk")  # ���ֽ�ת��Ϊ�ַ���
        output_text.insert(tk.END, output)
        notebook.select(tab2)  # ��ת���ڶ���ѡ�
        output_text.see(tk.END)  # �������ı���ײ�
        messagebox.showinfo(WheelErrorMSG,
                            "Run " + command + " Failed\nPlease check your config.\nOutput:\n" + output)
    except Exception:
        messagebox.showinfo(WheelErrorMSG, "Run " + command + " Failed\n������������Ƿ���ȷ.")


def handle_gametype_command(command):
    # ���ȼ���Ƿ���ڶ�Ӧ�������ļ�
    config_fle_name_path = "NicoMicoModTool/Presets/" + command + "Config.json"
    if os.path.exists(config_fle_name_path):
        # ��ȡ���������ļ�֮ǰ�Ƿ�Ҫ���浱ǰ�����ļ���Ĭ�ϱ����
        result = messagebox.askokcancel(WheelInfoMSG, "�л�����ǰ��ҪУ�鲢���浱ǰ������")
        if result:
            check_result = check_and_set_and_save_config()
            # ��ȡ�����ö�Ӧ�����ļ�
            if check_result:
                read_json_and_set_config_tab(config_fle_name_path)
        else:
            read_json_and_set_config_tab(config_fle_name_path)
    else:
        result = messagebox.askokcancel(WheelInfoMSG, "�л�����ǰ��ҪУ�鲢���浱ǰ������")
        if result:
            check_result = check_and_set_and_save_config()
        global wheel_game_type
        wheel_game_type = command
        window.title(WheelName + "   ��ǰ��Ϸ����: " + command)
        clean_config()


def handle_file_command(command):
    if command == "���":
        clean_config()

    if command == "��":
        # ���ļ�ѡ�񴰿�
        file_path = askopenfilename(filetypes=[('JSON Files', '*.json')])
        if file_path != "":
            read_json_and_set_config_tab(file_path)

    if command == "����":
        save_result = check_and_set_and_save_config()
        if save_result:
            messagebox.showinfo(WheelInfoMSG, "���ñ���ɹ�")

    if command == "���Ϊ":
        file_path = asksaveasfilename(defaultextension=".json", filetypes=[('Json File', '*.json')])
        save_result = check_and_set_and_save_config(file_path)
        if save_result:
            messagebox.showinfo(WheelInfoMSG, "���ñ���ɹ�")


def handle_format_command(command):
    if command == "reverse":
        # �򿪶Ի���ѡ��ini�ļ�·��
        # ���ļ�ѡ�񴰿�
        file_path = askopenfilename(filetypes=[('Mod ini file', '*.ini')])

        if file_path.__contains__(" "):
            messagebox.showinfo(WheelErrorMSG, "Ҫ�����Mod�ļ�·�����ܺ����κοո�.")
        elif file_path != "":
            try:
                output = subprocess.check_output(wheel_path + " " + command + " " + file_path + " " + wheel_game_type
                                                 , shell=True)
                output = output.decode("gbk")  # ���ֽ�ת��Ϊ�ַ���
                output_text.insert(tk.END, output)
                notebook.select(tab2)  # ��ת���ڶ���ѡ�
                output_text.see(tk.END)  # �������ı���ײ�
                messagebox.showinfo(WheelInfoMSG, "Mod�������.")
            except subprocess.CalledProcessError as e:
                output = e.output.decode("gbk")
                output_text.insert(tk.END, output)
                notebook.select(tab2)
                output_text.see(tk.END)
                messagebox.showinfo(WheelErrorMSG, "Run " + command
                                    + " Failed\nPleae check your ini file format and GameType.\nOutput:\n" + output)


def create_menu():
    # ���������˵�
    menubar = tk.Menu(window)
    # �����ļ��˵�������Ӳ˵���
    file_menu = tk.Menu(menubar, tearoff=0)
    file_menu.add_command(label="���", command=lambda: handle_file_command("���"))
    file_menu.add_command(label="��", command=lambda: handle_file_command("��"))
    file_menu.add_command(label="����", command=lambda: handle_file_command("����"))
    file_menu.add_command(label="���Ϊ...", command=lambda: handle_file_command("���Ϊ"))

    menubar.add_cascade(label="����", menu=file_menu)

    # �����ļ��˵�������Ӳ˵���
    game_type_menu = tk.Menu(menubar, tearoff=0)

    # Unity����
    game_type_unity_menu = tk.Menu(menubar, tearoff=0)
    hi3_submenu = tk.Menu(game_type_unity_menu, tearoff=0)
    hi3_submenu.add_command(label="body", command=lambda: handle_gametype_command("HI3Body"))
    hi3_submenu.add_command(label="object", command=lambda: handle_gametype_command("HI3Object"))
    game_type_unity_menu.add_cascade(label="������", menu=hi3_submenu)

    gi_submenu = tk.Menu(game_type_unity_menu, tearoff=0)
    gi_submenu.add_command(label="body", command=lambda: handle_gametype_command("GIBody"))
    gi_submenu.add_command(label="bodyNPC", command=lambda: handle_gametype_command("GIBodyNPC"))
    gi_submenu.add_command(label="object", command=lambda: handle_gametype_command("GIObject"))
    gi_submenu.add_command(label="object2", command=lambda: handle_gametype_command("GIObject2"))
    game_type_unity_menu.add_cascade(label="ԭ��", menu=gi_submenu)

    hsr_submenu = tk.Menu(game_type_unity_menu, tearoff=0)
    hsr_submenu.add_command(label="body", command=lambda: handle_gametype_command("HSRBody"))
    hsr_submenu.add_command(label="body-enemy", command=lambda: handle_gametype_command("HSRBodyEnemy"))
    hsr_submenu.add_command(label="hair", command=lambda: handle_gametype_command("HSRHair"))
    hsr_submenu.add_command(label="weapon type1", command=lambda: handle_gametype_command("HSRWeapon"))
    hsr_submenu.add_command(label="weapon type2", command=lambda: handle_gametype_command("HSRWeaponType2"))
    hsr_submenu.add_command(label="weapon type3", command=lambda: handle_gametype_command("HSRWeaponType3"))
    hsr_submenu.add_command(label="object", command=lambda: handle_gametype_command("HSRObject"))
    hsr_submenu.add_command(label="object_ib", command=lambda: handle_gametype_command("HSRObjectIB"))

    game_type_unity_menu.add_cascade(label="����:�������", menu=hsr_submenu)

    zzz_submenu = tk.Menu(game_type_unity_menu, tearoff=0)
    zzz_submenu.add_command(label="body", command=lambda: handle_gametype_command("ZZZBody"))
    zzz_submenu.add_command(label="weapon", command=lambda: handle_gametype_command("ZZZ weapon"), state="disabled")
    zzz_submenu.add_command(label="weapon without blendweights",
                            command=lambda: handle_gametype_command("ZZZ weapon without blendweights"),
                            state="disabled")
    game_type_unity_menu.add_cascade(label="������", menu=zzz_submenu)

    nbp_submenu = tk.Menu(game_type_unity_menu, tearoff=0)
    nbp_submenu.add_command(label="body", command=lambda: handle_gametype_command("NBPBody"))
    nbp_submenu.add_command(label="object", command=lambda: handle_gametype_command("NBPObject"))
    nbp_submenu.add_command(label="weapon", command=lambda: handle_gametype_command("NBPWeapon"))
    game_type_unity_menu.add_cascade(label="�����޼�", menu=nbp_submenu)

    bs_submenu = tk.Menu(game_type_unity_menu, tearoff=0)
    bs_submenu.add_command(label="body", command=lambda: handle_gametype_command("BSBody"))
    bs_submenu.add_command(label="object", command=lambda: handle_gametype_command("BS weapon"), state="disabled")
    game_type_unity_menu.add_cascade(label="��Ѫӡ", menu=bs_submenu)

    gf2_submenu = tk.Menu(game_type_unity_menu, tearoff=0)
    gf2_submenu.add_command(label="body", command=lambda: handle_gametype_command("GF2Body"))
    gf2_submenu.add_command(label="leg", command=lambda: handle_gametype_command("GF2Leg"))
    gf2_submenu.add_command(label="weapon", command=lambda: handle_gametype_command("GF2Weapon"))
    gf2_submenu.add_command(label="face", command=lambda: handle_gametype_command("GF2Face"))
    gf2_submenu.add_command(label="object", command=lambda: handle_gametype_command("GF2Object"))
    gf2_submenu.add_command(label="objectR32", command=lambda: handle_gametype_command("GF2ObjectR32"))

    game_type_unity_menu.add_cascade(label="��Ůǰ��2", menu=gf2_submenu)

    game_type_menu.add_cascade(label="Unity", menu=game_type_unity_menu)

    # UE4 type
    # game_type_ue4_menu = tk.Menu(menubar, tearoff=0)
    # KALABIYAU
    # kalabiyau_submenu = tk.Menu(game_type_ue4_menu, tearoff=0)
    # kalabiyau_submenu.add_command(label="body", command=lambda: handle_gametype_command("KBYBody"))
    # game_type_ue4_menu.add_cascade(label="��������", menu=kalabiyau_submenu)
    # game_type_menu.add_cascade(label="UE4", menu=game_type_ue4_menu)

    menubar.add_cascade(label="��Ϸ����", menu=game_type_menu)

    run_menu = tk.Menu(menubar, tearoff=0)
    run_menu.add_command(label="�ں�ib��vb0ģ���ļ�", command=lambda: handle_run_command("merge"))
    run_menu.add_command(label="�ָ�ib��vb�ļ�ΪMod", command=lambda: handle_run_command("split"))
    run_menu.add_command(label="����VertexShader���", command=lambda: handle_run_command("generateBasicCheck"))
    run_menu.add_command(label="����IB Skip Mod", command=lambda: handle_run_command("skipModGenerate"))
    run_menu.add_command(label="����DrawIB������������SKIP", command=lambda: handle_run_command("listDrawIBIndexSkip"))
    run_menu.add_command(label="�ƶ�IB����ļ�", command=lambda: handle_run_command("moveIBRelatedFiles"))
    menubar.add_cascade(label="����", menu=run_menu)

    format_menu = tk.Menu(menubar, tearoff=0)
    reverse_menu = tk.Menu(format_menu, tearoff=0)
    reverse_menu.add_command(label="����Mod", command=lambda: handle_format_command("reverse"))
    # reverse_menu.add_command(label="���һMod", command=lambda: handle_format_command("Help"), state="disabled")
    # reverse_menu.add_command(label="�����л�Mod", command=lambda: handle_format_command("Help"), state="disabled")
    format_menu.add_cascade(label="����Mod", menu=reverse_menu)

    # format_menu.add_command(label="����Ϊ.3dm��ʽ", command=lambda: handle_format_command("Help"), state="disabled")
    # format_menu.add_command(label="����.3dm��ʽ", command=lambda: handle_format_command("Help"), state="disabled")
    # format_menu.add_command(label=".ib�ļ�����ת��", command=lambda: handle_format_command("Help"), state="disabled")

    menubar.add_cascade(label="��ʽת��", menu=format_menu)

    # ���˵���ӵ�������
    window.config(menu=menubar)


def toggle_textbox():
    if checkbox_var_skip_ib_list.get():
        text_box_skip_ib_list.configure(state=tk.NORMAL)
        text_box_skip_ib_list.configure(state=tk.NORMAL, bg="white")
    else:
        text_box_skip_ib_list.configure(state=tk.DISABLED)
        text_box_skip_ib_list.configure(state=tk.DISABLED, bg="light gray")


def toggle_outline():
    if checkbox_var_color_rgb_a.get():
        text_box_color_rgb_a.configure(state=tk.NORMAL)
        text_box_color_rgb_a.configure(state=tk.NORMAL, bg="white")
    else:
        text_box_color_rgb_a.configure(state=tk.DISABLED)
        text_box_color_rgb_a.configure(state=tk.DISABLED, bg="light gray")


def toggle_tangent():
    if checkbox_var_tangent.get():
        combobox_tangent.configure(state=tk.NORMAL)

    else:
        combobox_tangent.set("None")
        combobox_tangent.configure(state=tk.DISABLED)


def toggle_texture_diffuse():
    if checkbox_var_texture_diffuse.get():
        text_box_texture_diffuse.configure(state=tk.NORMAL)
        text_box_texture_diffuse.configure(state=tk.NORMAL, bg="white")
    else:
        text_box_texture_diffuse.configure(state=tk.DISABLED)
        text_box_texture_diffuse.configure(state=tk.DISABLED, bg="light gray")


def toggle_texture_normal():
    if checkbox_var_texture_normal.get():
        text_box_texture_normal.configure(state=tk.NORMAL)
        text_box_texture_normal.configure(state=tk.NORMAL, bg="white")
    else:
        text_box_texture_normal.configure(state=tk.DISABLED)
        text_box_texture_normal.configure(state=tk.DISABLED, bg="light gray")


def toggle_texture_light():
    if checkbox_var_texture_light.get():
        text_box_texture_light.configure(state=tk.NORMAL)
        text_box_texture_light.configure(state=tk.NORMAL, bg="white")
    else:
        text_box_texture_light.configure(state=tk.DISABLED)
        text_box_texture_light.configure(state=tk.DISABLED, bg="light gray")


def clean_config():
    text_box_mod_name.delete("1.0", "end")
    text_box_draw_ib.delete("1.0", "end")

    skip_ib_list = []
    skip_ib_list_text = ""
    for skip_ib in skip_ib_list:
        if skip_ib != "":
            skip_ib_list_text = skip_ib_list_text + skip_ib + ","
    skip_ib_list_text = skip_ib_list_text[0:-1]

    text_box_skip_ib_list.configure(state='normal')
    text_box_skip_ib_list.delete("1.0", "end")
    text_box_skip_ib_list.configure(state='disabled', bg="light gray")
    if skip_ib_list_text != "":
        checkbox_var_skip_ib_list.set(True)
    else:
        checkbox_var_skip_ib_list.set(False)

    text_box_output_folder.configure(state='normal')
    text_box_output_folder.delete("1.0", "end")
    text_box_output_folder.configure(state='disabled')

    text_box_loader_folder.configure(state='normal')
    text_box_loader_folder.delete("1.0", "end")
    text_box_loader_folder.configure(state='disabled')

    text_box_fa_folder.configure(state='normal')
    text_box_fa_folder.delete("1.0", "end")
    text_box_fa_folder.configure(state='disabled')

    # Cancel the selection of color checkbox and clean and set status to disable.
    checkbox_var_color_rgb_a.set(False)
    text_box_color_rgb_a.configure(state='normal')
    text_box_color_rgb_a.delete("1.0", "end")
    text_box_color_rgb_a.configure(state='disabled', bg="light gray")

    # Cancel the selection of tangent checkbox and clean and set combox status to disable.
    checkbox_var_tangent.set(False)
    combobox_tangent.set("None")
    combobox_tangent.configure(state='disabled')

    # Cancel the selection of texture diffuse checkbox and clean and set status to disable.
    checkbox_var_texture_diffuse.set(False)
    text_box_texture_diffuse.configure(state='normal')
    text_box_texture_diffuse.delete("1.0", "end")
    text_box_texture_diffuse.configure(state='disabled', bg="light gray")

    # Cancel the selection of texture normal checkbox and clean and set status to disable.
    checkbox_var_texture_normal.set(False)
    text_box_texture_normal.configure(state='normal')
    text_box_texture_normal.delete("1.0", "end")
    text_box_texture_normal.configure(state='disabled', bg="light gray")

    # Cancel the selection of texture light checkbox and clean and set status to disable.
    checkbox_var_texture_light.set(False)
    text_box_texture_light.configure(state='normal')
    text_box_texture_light.delete("1.0", "end")
    text_box_texture_light.configure(state='disabled', bg="light gray")

    # clean the log in output tab.
    output_text.delete("1.0", "end")
    notebook.select(tab1)


def check_and_set_and_save_config(output_json_path=""):
    # Check all the configs in config tab.
    # ModName can not be empty.
    content_mod_name = text_box_mod_name.get("1.0", "end-1c").strip()  # ��ȡ�ı����е�����
    if content_mod_name == "":
        messagebox.showinfo("Config Error", "ModNameΪ�գ�������ModName")
        return False

    if has_chinese(content_mod_name):
        messagebox.showinfo("Config Error", "ModName���ܳ�������")
        return False

    content_draw_ib = text_box_draw_ib.get("1.0", "end-1c").strip()  # ��ȡ�ı����е�����
    if not hash_format_check(content_draw_ib, "DrawIB"):
        return False
    content_output_folder = text_box_output_folder.get("1.0", "end-1c").strip()  # ��ȡ�ı����е�����
    if content_output_folder == "":
        messagebox.showinfo("Config Error", "OutputFolderΪ�գ�������OutputFolder")
        return False

    content_loader_folder = text_box_loader_folder.get("1.0", "end-1c").strip()  # ��ȡ�ı����е�����
    if content_loader_folder == "":
        messagebox.showinfo("Config Error", "LoaderFolderΪ�գ�������LoaderFolder")
        return False

    content_fa_folder = text_box_fa_folder.get("1.0", "end-1c").strip()  # ��ȡ�ı����е�����
    if content_fa_folder == "":
        messagebox.showinfo("Config Error", "FrameAnalyseFolderΪ�գ�������FrameAnalyseFolder")
        return False

    content_rgba = text_box_color_rgb_a.get("1.0", "end-1c").strip()  # ��ȡ�ı����е�����
    # ��ѡ�˲����жϣ�����ѡ�Ļ�����ȫ����Ϊdefault
    if checkbox_var_color_rgb_a.get():
        if not contains_only_digits(content_rgba):
            messagebox.showinfo("Config Error", "outlineֵ(rgb_a)ֻ������Ϊ0��255֮�������")
            return False

        if int(content_rgba) < 0 or int(content_rgba) > 255:
            messagebox.showinfo("Config Error", "outlineֵ(rgb_a)ֻ������Ϊ0��255֮�������")
            return False

    # ��ѡ�˲����ж�
    content_skip_ib_list = []
    if checkbox_var_skip_ib_list.get():
        content_skip_ib_list_str = text_box_skip_ib_list.get("1.0", "end-1c").strip()
        if has_chinese(content_skip_ib_list_str):
            messagebox.showinfo("Config Error", "Skip IB List�в��ܳ�������")
            return False

        if content_skip_ib_list_str != "":
            content_skip_ib_list = content_skip_ib_list_str.split(",")
            # ��ÿ��hashֵ�����жϲ��ܳ������ĺͳ��ȱ���Ϊ8
            for skip_ib in content_skip_ib_list:
                if skip_ib == "":
                    messagebox.showinfo("Config Error", "SkipIBList�к���Ϊ�յ�IB����������")
                    return False

                if len(skip_ib) != 8:
                    messagebox.showinfo("Config Error", "SkipIBList�е�IB��Hashֵ�����ȱ���Ϊ8")
                    return False

    # �����ȷ���Ͱ������ļ�д��3Dmgigoto-WheelĿ¼�µ�Config.json�ֱ�Ӹ��ǣ�����ȷ��������
    # ��ȡConfig.json��Ϊģ�������ļ�
    config_json_file = open(config_json_path, "r")
    config_json = json.load(config_json_file)
    config_json_file.close()
    # ��ʼ������ֵ
    config_json["Preset"]["ModName"] = content_mod_name
    config_json["Preset"]["DrawIB"] = content_draw_ib
    config_json["Preset"]["OutputFolder"] = content_output_folder
    config_json["Preset"]["LoaderFolder"] = content_loader_folder
    config_json["Preset"]["FrameAnalyseFolder"] = content_fa_folder
    config_json["Preset"]["GameType"] = wheel_game_type
    # ����skip ib list���ҹ�ѡ�˲����ã�����ѡ������дʲô���ݶ�����Ϊ�գ���ֹ��Ⱦ����
    if checkbox_var_skip_ib_list.get():
        config_json["SkipIBList"] = content_skip_ib_list
    else:
        config_json["SkipIBList"] = []

    # ����outline��û��ѡ����Ϊdefault
    if checkbox_var_color_rgb_a.get():
        config_json["Color"]["rgb_a"] = content_rgba
    else:
        config_json["Color"]["rgb_a"] = "default"

    if checkbox_var_tangent.get():
        if combobox_tangent.get() != "None":
            config_json["TangentAlgorithm"] = combobox_tangent.get()
        else:
            config_json["TangentAlgorithm"] = ""
    else:
        config_json["TangentAlgorithm"] = ""

    # Set texture diffuse, if not selected we set it to "".
    content_texture_diffuse = text_box_texture_diffuse.get("1.0", "end-1c").strip()
    if checkbox_var_texture_diffuse.get():
        if not hash_format_check(content_texture_diffuse, "DiffuseMap��Hashֵ"):
            return False

        if content_texture_diffuse != "":

            config_json["TextureDict"]["diffuse.dds"] = content_texture_diffuse
        else:
            config_json["TextureDict"]["diffuse.dds"] = ""
    else:
        config_json["TextureDict"]["diffuse.dds"] = ""

    # Set texture normal, if not selected we set it to "".
    content_texture_normal = text_box_texture_normal.get("1.0", "end-1c").strip()

    if checkbox_var_texture_normal.get():
        if not hash_format_check(content_texture_normal, "NormalMap��Hashֵ"):
            return False

        if content_texture_normal != "":
            config_json["TextureDict"]["normal.dds"] = content_texture_normal
        else:
            config_json["TextureDict"]["normal.dds"] = ""
    else:
        config_json["TextureDict"]["normal.dds"] = ""

    # Set texture diffuse, if not selected we set it to "".
    content_texture_light = text_box_texture_light.get("1.0", "end-1c").strip()

    if checkbox_var_texture_light.get():
        if not hash_format_check(content_texture_light, "LightMap��Hashֵ"):
            return False
        if content_texture_light != "":
            config_json["TextureDict"]["light.dds"] = content_texture_light
        else:
            config_json["TextureDict"]["light.dds"] = ""
    else:
        config_json["TextureDict"]["light.dds"] = ""

    # д��json�������ļ�
    with open(config_json_path, "w") as config_json_output_file:
        json.dump(config_json, config_json_output_file)

    # ������֮�󣬸���GameType����Config.json���Ʋ�����д��PresetsĿ¼�µĶ�ӦGameTypeConfig.json��
    preset_json_path = "NicoMicoModTool/Presets/" + wheel_game_type + "Config.json"
    # �������ʹ��shutil.copy2�ᵼ�¸��Ƴ����������룬������������дһ��
    # shutil.copy2(wheel_path, target_json_name)
    # д֮ǰ������ڣ���ɾ��
    if os.path.exists(preset_json_path):
        os.remove(preset_json_path)

    with open(preset_json_path, "w") as config_json_output_file:
        json.dump(config_json, config_json_output_file)

    # ����ƶ������Ŀ¼����������һ�ݵ����Ŀ¼��
    if output_json_path != "":
        with open(output_json_path, "w") as config_json_output_file:
            json.dump(config_json, config_json_output_file)

    # ��󷵻�True����ʼִ�ж�Ӧ�߼�����
    return True


def read_json_and_set_config_tab(filepath):
    # ��Config.json�ж�ȡ���ã���ȡ����д�����������
    with open(filepath, 'r') as file:
        # ��ȡ�ļ�����
        config_json = json.load(file)
        # ����GameType
        game_type = config_json["Preset"]["GameType"]
        window.title(WheelName + "   ��ǰ��Ϸ����: " + game_type)

        global wheel_game_type
        wheel_game_type = game_type

        text_box_mod_name.delete("1.0", "end")
        text_box_mod_name.insert("1.0", config_json["Preset"]["ModName"])

        text_box_draw_ib.delete("1.0", "end")
        text_box_draw_ib.insert("1.0", config_json["Preset"]["DrawIB"])

        skip_ib_list = config_json["SkipIBList"]
        skip_ib_list_text = ""
        for skip_ib in skip_ib_list:
            if skip_ib != "":
                skip_ib_list_text = skip_ib_list_text + skip_ib + ","
        skip_ib_list_text = skip_ib_list_text[0:-1]
        text_box_skip_ib_list.configure(state='normal')  # ��״̬����Ϊ����
        text_box_skip_ib_list.delete("1.0", "end")
        text_box_skip_ib_list.insert("1.0", skip_ib_list_text)
        text_box_skip_ib_list.configure(state='disabled')  # ��״̬��������Ϊ����
        if skip_ib_list_text != "":
            checkbox_var_skip_ib_list.set(True)
        else:
            checkbox_var_skip_ib_list.set(False)

        text_box_output_folder.configure(state='normal')
        text_box_output_folder.delete("1.0", "end")
        text_box_output_folder.insert("1.0",config_json["Preset"]["OutputFolder"])
        text_box_output_folder.configure(state='disabled')

        text_box_loader_folder.configure(state='normal')
        text_box_loader_folder.delete("1.0", "end")
        text_box_loader_folder.insert("1.0", config_json["Preset"]["LoaderFolder"])
        text_box_loader_folder.configure(state='disabled')

        text_box_fa_folder.configure(state='normal')
        text_box_fa_folder.delete("1.0", "end")
        text_box_fa_folder.insert("1.0", config_json["Preset"]["FrameAnalyseFolder"])
        text_box_fa_folder.configure(state='disabled')
        # ��ȡ������rgb_a
        str_rgb_a = config_json["Color"]["rgb_a"]
        if str_rgb_a != "default":
            checkbox_var_color_rgb_a.set(True)
            text_box_color_rgb_a.configure(state='normal')
            text_box_color_rgb_a.delete("1.0", "end")
            text_box_color_rgb_a.insert("1.0", str_rgb_a)
        else:
            checkbox_var_color_rgb_a.set(False)
            text_box_color_rgb_a.configure(state='normal')
            text_box_color_rgb_a.delete("1.0", "end")

        # ��ȡ������tangent
        str_tangent = config_json["TangentAlgorithm"]
        if str_tangent != "":
            checkbox_var_tangent.set(True)
            combobox_tangent.configure(state='normal')
            combobox_tangent.set(str_tangent)
        else:
            checkbox_var_tangent.set(False)
            combobox_tangent.set("None")
            combobox_tangent.configure(state='disabled')

        # Read and set texture diffuse
        str_texture_diffuse = config_json["TextureDict"]["diffuse.dds"]
        if str_texture_diffuse != "":
            checkbox_var_texture_diffuse.set(True)
            text_box_texture_diffuse.configure(state="normal")
            text_box_texture_diffuse.delete("1.0", "end")
            text_box_texture_diffuse.insert("1.0", str_texture_diffuse)

        else:
            checkbox_var_texture_diffuse.set(False)
        toggle_texture_diffuse()

        # Read and set normal diffuse
        str_texture_normal = config_json["TextureDict"]["normal.dds"]
        if str_texture_normal != "":
            checkbox_var_texture_normal.set(True)
            text_box_texture_normal.configure(state="normal")
            text_box_texture_normal.delete("1.0", "end")
            text_box_texture_normal.insert("1.0", str_texture_normal)

        else:
            checkbox_var_texture_normal.set(False)
        toggle_texture_normal()

        # Read and set texture diffuse
        str_texture_light = config_json["TextureDict"]["light.dds"]
        if str_texture_light != "":
            checkbox_var_texture_light.set(True)
            text_box_texture_light.configure(state="normal")
            text_box_texture_light.delete("1.0", "end")
            text_box_texture_light.insert("1.0", str_texture_light)

        else:
            checkbox_var_texture_light.set(False)
        toggle_texture_light()

        # ���output��Ķ���
        output_text.delete("1.0", "end")
        notebook.select(tab1)


if __name__ == "__main__":
    # Create NicoMicoModTool window
    window = tk.Tk()
    window.title(WheelName + "   ��ǰ��Ϸ����: None")

    # ע�ᴰ�ڹر�ʱ�Ļص�����
    window.protocol("WM_DELETE_WINDOW", on_closing)

    # ��ȡ��Ļ��Ⱥ͸߶�
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    # Set window size and position
    window_width = 800
    window_height = 600
    x = (screen_width - window_width) // 2
    y = (screen_height - window_height) // 2

    # Set window position to the center of screen.
    window.geometry(f"{window_width}x{window_height}+{x}+{y}")

    # menu define
    create_menu()

    # ����ѡ��ؼ�
    notebook = ttk.Notebook(window)
    notebook.pack(fill=tk.BOTH, expand=True)

    # ����������д�����ļ���ѡ�
    tab1 = ttk.Frame(notebook)
    notebook.add(tab1, text="Mod����")

    # -------------------------Mod Name------------------------------
    frame_mod_name = tk.Frame(tab1)
    frame_mod_name.pack(anchor=tk.W)

    label_mod_name = ttk.Label(frame_mod_name, text="ModName")
    label_mod_name.pack(side=tk.LEFT)

    text_box_mod_name = tk.Text(frame_mod_name, height=1, width=70)
    text_box_mod_name.pack(side=tk.LEFT)

    # -------------------------Draw IB------------------------------
    # ����һ����ܣ��������ɹ�ѡ����ı���
    frame_draw_ib = tk.Frame(tab1)
    frame_draw_ib.pack(anchor=tk.W)

    label_draw_ib = ttk.Label(frame_draw_ib, text="DrawIB")
    label_draw_ib.pack(side=tk.LEFT)

    text_box_draw_ib = tk.Text(frame_draw_ib, height=1, width=10)
    text_box_draw_ib.pack(side=tk.LEFT)

    # -------------------------Skip IB List------------------------------
    # ����һ����ܣ��������ɹ�ѡ����ı���
    frame_skip_ib_list = tk.Frame(tab1)
    frame_skip_ib_list.pack(anchor=tk.W)

    # ���� BooleanVar �������ڿ���SkipIBList��ѡ��Ĺ�ѡ״̬
    checkbox_var_skip_ib_list = tk.BooleanVar(value=False)

    # ������ѡ��
    checkbox_skip_ib_list = ttk.Checkbutton(frame_skip_ib_list, text="Skip IB List"
                                            , variable=checkbox_var_skip_ib_list, command=toggle_textbox)
    checkbox_skip_ib_list.pack(side=tk.LEFT)

    text_box_skip_ib_list = tk.Text(frame_skip_ib_list, height=1, width=100,state=tk.DISABLED, bg="light gray")
    text_box_skip_ib_list.pack(side=tk.LEFT)

    # -----------------����ָ����ָ�һ��------------------------
    separator = ttk.Separator(window, orient="horizontal")
    separator.pack(fill="x", padx=10, pady=10)
    separator.pack(after=frame_skip_ib_list)  # ���ָ���������frame_skip_ib_list��ܵ��·�

    # -------------------------Output Folder------------------------------
    frame_output_folder = tk.Frame(tab1)
    frame_output_folder.pack(anchor=tk.W)

    label_output_folder = ttk.Label(frame_output_folder, text="OutputFolder")
    label_output_folder.pack(side=tk.LEFT)

    text_box_output_folder = tk.Text(frame_output_folder, height=1, width=85, state=tk.DISABLED, bg="light gray")
    text_box_output_folder.pack(side=tk.LEFT)

    button_output_folder = tk.Button(frame_output_folder, text="Open", height=1
                                     , command=handle_open_output_folder_command)
    button_output_folder.pack(side=tk.LEFT)

    # -------------------------Loader Folder------------------------------
    frame_loader_folder = tk.Frame(tab1)
    frame_loader_folder.pack(anchor=tk.W)

    label_loader_folder = ttk.Label(frame_loader_folder, text="LoaderFolder")
    label_loader_folder.pack(side=tk.LEFT)

    text_box_loader_folder = tk.Text(frame_loader_folder, height=1, width=85, state=tk.DISABLED, bg="light gray")
    text_box_loader_folder.pack(side=tk.LEFT)

    button_loader_folder = tk.Button(frame_loader_folder, text="Open", height=1
                                     , command=handle_open_loader_folder_command)
    button_loader_folder.pack(side=tk.LEFT)

    # -------------------------FrameAnalyseFolder------------------------------
    frame_fa_folder = tk.Frame(tab1)
    frame_fa_folder.pack(anchor=tk.W)

    label_fa_folder = ttk.Label(frame_fa_folder, text="FrameAnalyseFolder")
    label_fa_folder.pack(side=tk.LEFT)

    text_box_fa_folder = tk.Text(frame_fa_folder, height=1, width=80, state=tk.DISABLED, bg="light gray")
    text_box_fa_folder.pack(side=tk.LEFT)

    button_fa_folder = tk.Button(frame_fa_folder, text="Open", height=1, command=handle_open_fa_folder_command)
    button_fa_folder.pack(side=tk.LEFT)

    # -----------------����ָ����ָ�һ��------------------------
    separator = ttk.Separator(window, orient="horizontal")
    separator.pack(fill="x", padx=10, pady=10)
    separator.pack(after=frame_fa_folder)  # ���ָ���������frame_skip_ib_list��ܵ��·�

    # -------------------------COLOR reset------------------------------
    # ����һ����ܣ��������ɹ�ѡ����ı���
    frame_color = tk.Frame(tab1)
    frame_color.pack(anchor=tk.W)

    # ���� BooleanVar �������ڿ���SkipIBList��ѡ��Ĺ�ѡ״̬
    checkbox_var_color_rgb_a = tk.BooleanVar(value=False)

    # ������ѡ��
    checkbox_color_rgb_a = ttk.Checkbutton(frame_color, text="Set outline (RGBA)", variable=checkbox_var_color_rgb_a,
                                           command=toggle_outline)
    checkbox_color_rgb_a.pack(side=tk.LEFT)

    text_box_color_rgb_a = tk.Text(frame_color, height=1, width=30, state=tk.DISABLED, bg="light gray")
    text_box_color_rgb_a.pack(side=tk.LEFT)

    # -------------------------recalculate TANGENT------------------------------
    frame_tangent = tk.Frame(tab1)
    frame_tangent.pack(anchor=tk.W)

    checkbox_var_tangent = tk.BooleanVar(value=False)
    checkbox_tangent = ttk.Checkbutton(frame_tangent, text="Recalculate TANGENT", variable=checkbox_var_tangent,
                                           command=toggle_tangent)
    checkbox_tangent.pack(side=tk.LEFT)

    # ���������б�
    combobox_tangent = ttk.Combobox(frame_tangent, values=["None", "ignore_tangent",
                                                           "ignore_tangent_reverse","ignore_tangent_original"])
    combobox_tangent.pack(side=tk.LEFT)

    # ����ѡ���¼�
    combobox_tangent.bind("<<ComboboxSelected>>", on_select_tangent)

    # -----------------����ָ����ָ�һ��------------------------
    separator = ttk.Separator(window, orient="horizontal")
    separator.pack(fill="x", padx=10, pady=10)
    separator.pack(after=frame_tangent)  # ���ָ���������frame_tangent��ܵ��·�

    # -------------------------��ͼ��λ����------------------------------
    # diffuse
    frame_texture_diffuse = tk.Frame(tab1)
    frame_texture_diffuse.pack(anchor=tk.W)

    checkbox_var_texture_diffuse = tk.BooleanVar(value=False)
    checkbox_texture_diffuse = ttk.Checkbutton(frame_texture_diffuse, text="Diffuse Map"
                                               , variable=checkbox_var_texture_diffuse, command=toggle_texture_diffuse)
    checkbox_texture_diffuse.pack(side=tk.LEFT)
    text_box_texture_diffuse = tk.Text(frame_texture_diffuse, height=1, width=10, state=tk.DISABLED, bg="light gray")
    text_box_texture_diffuse.pack(side=tk.LEFT)

    # normal
    frame_texture_normal = tk.Frame(tab1)
    frame_texture_normal.pack(anchor=tk.W)

    checkbox_var_texture_normal = tk.BooleanVar(value=False)
    checkbox_texture_normal = ttk.Checkbutton(frame_texture_normal, text="Normal Map"
                                              , variable=checkbox_var_texture_normal, command=toggle_texture_normal)
    checkbox_texture_normal.pack(side=tk.LEFT)
    text_box_texture_normal = tk.Text(frame_texture_normal, height=1, width=10, state=tk.DISABLED, bg="light gray")
    text_box_texture_normal.pack(side=tk.LEFT)

    # light
    frame_texture_light = tk.Frame(tab1)
    frame_texture_light.pack(anchor=tk.W)

    checkbox_var_texture_light = tk.BooleanVar(value=False)
    checkbox_texture_light = ttk.Checkbutton(frame_texture_light, text="Light Map"
                                             , variable=checkbox_var_texture_light, command=toggle_texture_light)
    checkbox_texture_light.pack(side=tk.LEFT)
    text_box_texture_light = tk.Text(frame_texture_light, height=1, width=10, state=tk.DISABLED, bg="light gray")
    text_box_texture_light.pack(side=tk.LEFT)

    # -------------------------output tab------------------------------
    # ��������������н����ѡ�
    tab2 = ttk.Frame(notebook)
    notebook.add(tab2, text="������Ϣ")

    # ����output�ı���Ĺ�����
    scrollbar = tk.Scrollbar(tab2)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    # ����output�ı���
    output_text = tk.Text(tab2, height=10, width=50)
    output_text.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

    # ����output�ı���Ĺ�������output�ı���
    output_text.config(yscrollcommand=scrollbar.set)
    scrollbar.config(command=output_text.yview)

    # -------------------------������ѡ� mod������------------------------------
    # ����mod����ѡ�
    # tab3 = ttk.Frame(notebook)
    # notebook.add(tab3, text="Mod����")

    '''
    TODO
    ��λMods�ļ��У����ɸ���ɫԤ��Ŀ¼
    mod�ŵ���������Զ�ʶ���и��б����ѡ������ر�ָ��mod������һ��ȫ��������һ��ȫ���ر�
    ���Ը�ÿ��modָ��Ԥ��ͼ�����Ը���Ԥ��ͼ
    ���Ը���ͼ��ѡ���ɫ
    '''

    # �����ô���֮�󣬶�ȡĬ�ϵ������ļ�
    default_config_path = "NicoMicoModTool/Config.json"
    if os.path.exists(default_config_path):
        read_json_and_set_config_tab(default_config_path)

    # �������¼�ѭ��
    window.mainloop()

