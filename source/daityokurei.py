import tkinter as tk
from tkinter import messagebox
import random

def get_debuff_number(first =True):
    """
    女王の大勅令で付与されるデバフ（歩数）
    """
    num_0 = random.randrange(2,5)#出る数値は2~4
    num_1 = max(min(random.randrange(5,8) - num_0,4),2) #数値の合計は5~7
    perm = [num_0,num_1]
    random.shuffle(perm)#このロジックだと片方に数値が寄るっぽいので、シャッフル
    
    if (sum(perm)==6) and (random.random()>0.2) and first:
        #このやり方だと6が多すぎ
        perm = get_debuff_number(first=False)
        
    
    num_0,num_1 = perm[0],perm[1]
    return (num_0,num_1)


def get_step_number():
    """
    敵の歩数。
    
    判明しているルール
    - 1~3の値
    - 南北の場合は(3,3)は無いらしい
    - たぶん(1,1)もない
    """
    while True:
        step_number =  [random.randrange(1,4) for _ in range(2)]
        if not (step_number==[3,3]) and not (step_number==[1,1]):
            return step_number[0],step_number[1]
        
class Application(tk.Frame):
    
    def __init__(self,master=None):
        super().__init__(master)
        self.master = master
            
        """
        phase
        0:初期状態
        1:プレイヤー初期位置決定
        2:１回目移動後
        3:２回目移動後
        """

#         self.master.wm_attributes("-transparentcolor", 'grey')
    
        self.start()
    
    def start(self):
        self.master.title("女王の大勅令練習用アプリ！")
        self.master.geometry("500x500")
        self.pack()
        self.create_widgets()
        
    def all_reset(self):
        self.destroy()
        super().__init__(self.master)
        self.start()
        
    def create_widgets(self):

        self.phase=0
        self.player_current = (None,None)       
        self.lb = tk.Label(self,
                          font=("MSゴシック", "25", "bold"))
        
        
        self.lb["text"] = "女王の大勅令練習用アプリ！"
        self.lb.pack(side="top")
        
        self.debuff_num_text = tk.Label(self,font=("MSゴシック", "20", "bold"))
        
        self.debuff_num= get_debuff_number()
        
        self.debuff_num_text["text"] = f"１回目:{self.debuff_num[0]}歩   2回目:{self.debuff_num[1]}歩"
        self.debuff_num_text.pack(side="top")
        
        
#         self.en = tk.Entry(self)
#         self.en.pack()
#         self.en.focus_set()
        
#         self.bt = tk.Button(self)
        
#         self.bt["text"] = "リセット"
#         self.bt["command"] = self.all_reset
#         self.bt.pack(side="bottom")
        
        self.make_grid()

        self.frame.pack()
        
#         w = tk.Canvas(self.frame, width=250, height=200)
#         w.create_rectangle(0, 0, 100, 100, fill="blue", outline = 'blue')
#         w.create_rectangle(50, 50, 100, 100, fill="red", outline = 'blue') 
#         w.pack()
        
    def print_txtval(self):
        val_en = self.en.get()
        print(val_en)
        
    def count_step(self,col,row):
        """
        歩数関係の処理
        """
        col_preb,row_preb = self.player_current[0],self.player_current[1]
        self.player_preb = (col_preb,row_preb)
        self.player_current = (col,row)
            
        if not (col_preb==None and row_preb==None):
            #ちゃんと歩けてたか
            debuff_num = self.debuff_num[self.phase-1]
            
            step_num = abs(col-col_preb) + abs(row-row_preb)
            if step_num!=debuff_num:

                messagebox.showwarning("You Died","歩数ミス!!!")
                return False
        return True
            
    def push_grid(self,col,row):
        """
        ボタンによって反応をかえる方法参考
        https://qiita.com/shinno1993/items/a1ded967a84d0901866d
        """
        def inner():
            """マス目ボタンを押したときの挙動"""
            
            
                
            
            if self.phase>=3:
                self.all_reset()
            else:
                
                result = self.count_step(col,row)
                if not result:
                    self.all_reset()
                    return 
                    
                button = self.grid_list[col + row*5]

                if self.phase==0:
                    text ="start"
                elif self.phase ==1:
                    text ="1歩目"
                elif self.phase==2:
                    text ="2歩目"
                else:
                    text ="___"

                button["bg"]="#0dd"
                button["text"]=text
                self.enter_phase()
            
        return inner
        
    def make_grid(self):
        """女王の大勅令のマス作成
        マスは全部ボタンの予定"""
        self.scale=50
        
        

        self.frame = tk.Frame(self,
                              width =self.scale*7,
                              height=self.scale*7,
#                               background="#0ef"

                             )
        
#         self.main_window = self.canvas.create_window(0,0,
#                                                     height = self.scale*7,
#                                                      width = self.scale*7,
#                                                      window=self.frame,
# #                                                      anchor='nw'
#                                                     )
        goal_nums = [2,22]
        random.shuffle(goal_nums)
        goal_num = goal_nums[0]
        self.goal_num = goal_num
        grid_list = []
        for i in range(25):
            if i == goal_num:
                color="#0f0"
            elif i%2==0:
                color ="#fff"
            else:
                color="#888"
            col = i%5
            row = i//5
            
            grid = tk.Button(self.frame,
                             text=("ゴール" if i==self.goal_num else ""),
                            background=color,
                            command=self.push_grid(col,row),
                            borderwidth=2)
#             grid.grid(column=i%5,row=i//5)
            
            grid.place(x=self.scale+self.scale*(col),
                       y=self.scale+self.scale*(row),
                       width = self.scale,
                       height= self.scale
                      )
            grid_list.append(grid)
        self.grid_list = grid_list
#         self.frame.pack()    
        
#         self.canvas = tk.Canvas(
#                 self,
#                 width = self.scale*7,
#                 height = self.scale*7,
#             bd=0, highlightthickness=0
                
#         )
#         self.canvas.place(x=50,y=50)
        
        self.set_enemy()

        self.set_arrow()

        
    def set_enemy(self):
        """外側の敵の配置。
        南北・東西、それぞれパターンがあるからどうしよう
        
        西:enemy_w
        東:enemy_e
        
        北:enemy_n
        南:enemy_s
        
        でいいか
        北・西の敵の初期位置がx,y=0,0に近いか否かで設定
        
        place_ns=0なら敵_北は→,1なら敵_南は←ってのがややこしい
        """
        
        enemy_color="#d88"
        

        step_n,step_s = get_step_number()
        
        place_ns = random.randrange(0,2) #boolじゃないほうが楽かな
        self.enemy_n = tk.Label(self.frame,
                           text=f"{step_n}",
                           background=enemy_color,
                               font=("MSゴシック", "14", "bold")
                               )
        self.enemy_n.place(x=self.scale*2 + place_ns*(self.scale*2),
                      y=0,
                      width = self.scale,
                      height= self.scale
                     )
        
        
        self.enemy_s = tk.Label(self.frame,
                           text=f"{step_s}",
                           background=enemy_color,
                               font=("MSゴシック", "14", "bold")
                               )
        self.enemy_s.place(x=self.scale*4 + place_ns*(-self.scale*2),
                      y=self.scale*6,
                      width = self.scale,
                      height= self.scale
                     )
        
        
        
        #西、東の敵の配置
        step_e,step_w = get_step_number()
        place_ew = random.randrange(0,2) #boolじゃないほうが楽かな
        self.enemy_w = tk.Label(self.frame,
                           text=f"{step_w}",
                           background=enemy_color,
                               font=("MSゴシック", "14", "bold")
                               )
        self.enemy_w.place(x=0,
                      y=self.scale*2 + place_ew*(self.scale*2),
                      width = self.scale,
                      height= self.scale
                     )
        
        self.enemy_e = tk.Label(self.frame,
                           text=f"{step_e}",
                           background=enemy_color,
                               font=("MSゴシック", "14", "bold")
                               )
        self.enemy_e.place(x=self.scale*6,
                      y=self.scale*4 + place_ew*(-self.scale*2),
                      width = self.scale,
                      height= self.scale
                     )
        
        self.place_ns = place_ns
        self.place_ew = place_ew

        self.enemy_dict = {}
        self.enemy_dict["n"] = self.enemy_n
        self.enemy_dict["s"] = self.enemy_s
        self.enemy_dict["w"] = self.enemy_w
        self.enemy_dict["e"] = self.enemy_e
        
        self.step_dict = {}
        self.step_dict["n"] = step_n * (-1 if place_ns ==1 else 1)
        self.step_dict["s"] = step_s * (1 if place_ns ==1 else -1)
        self.step_dict["w"] = step_w * (-1 if place_ew ==1 else 1)
        self.step_dict["e"] = step_e * (1 if place_ew ==1 else -1)
        
        self.enemy_attack_position = {}
        self.enemy_attack_position["n"] = (3 if place_ns==1 else 1) + self.step_dict["n"]
        self.enemy_attack_position["s"] = (1 if place_ns==1 else 3) + self.step_dict["s"]
        self.enemy_attack_position["w"] = (3 if place_ew==1 else 1) + self.step_dict["w"]
        self.enemy_attack_position["e"] = (1 if place_ew==1 else 3) + self.step_dict["e"]


    def enemy_move(self,enemy_id,step_count=1):
        """
        動くかはわからん
        enemyはself.enemy_nなど
        stepはself.step_n,
        """
        
        
        enemy = self.enemy_dict[enemy_id]
        step = self.step_dict[enemy_id]
        enemy["bg"] ="#b00"
        
        x = enemy.winfo_x()
        y = enemy.winfo_y()
        
        for _ in range(step_count):
            if enemy_id in ["n","s"]:
    #             enemy.x +=step*self.scale
                x += (step*self.scale)/step_count
                enemy.place(x=x)
            else:
                y += (step*self.scale)/step_count
                enemy.place(y=y)


        result = self.attack_effect(enemy_id)
        return result
    
    def set_arrow(self):
        """
        次に動く敵のところに矢印をかきたい
        """
        if self.phase==0:
            #西の敵が移動する前。これは北・西で使い回す
            label_nw = "↑" if self.place_ew == 1 else "↓"
            self.arrow_nw = tk.Label(self.frame,
                           text=label_nw,
                               font=("MSゴシック", "18", "bold")
                               )
            self.arrow_nw.place(x=0,
                          y=self.scale*3,
                          width = self.scale,
                          height= self.scale
                         )
            
            #東の敵が移動する前。これは北・西で使い回す
            label_se = "↓" if self.place_ew == 1 else "↑"
            self.arrow_se = tk.Label(self.frame,
                           text=label_se,
                               font=("MSゴシック", "18", "bold")
                               )
            self.arrow_se.place(x=self.scale*6,
                          y=self.scale*3,
                          width = self.scale,
                          height= self.scale
                         )
            
        elif self.phase==1:
                        #西の敵が移動する前。これは北・西で使い回す
            label_nw = "←" if self.place_ns == 1 else "→"
            self.arrow_nw.place(x=self.scale*3,
                          y=0
                         )
            self.arrow_nw["text"] = label_nw
            
            #東の敵が移動する前。これは北・西で使い回す
            label_se = "→" if self.place_ns == 1 else "←"
            self.arrow_se.place(x=self.scale*3,
                          y=self.scale*6
                         )
            self.arrow_se["text"] = label_se
            
        else:
            pass
        


        
    def enter_phase(self):
        self.button_visual_reset()
        you_died = 0
        if self.phase==0:
            #東西の敵が移動する
            you_died += self.enemy_move("w")
            you_died += self.enemy_move("e")
        elif self.phase==1:
            #南北の敵が移動する
            self.arrow_nw.place(x=self.scale*30,
                          y=0
                         )
            self.arrow_se.place(x=self.scale*30,
                          y=0
                         )    
            you_died += self.enemy_move("n")
            you_died += self.enemy_move("s")  

        elif self.phase==2:
            #ゴールのはず
            col,row = self.player_current[0],self.player_current[1]
            player_pos = col + row*5
            if player_pos == self.goal_num:

                messagebox.showinfo("おめでとう！","おめでとう！！")
                self.all_reset()
                return
            else:
                you_died+=1


        
        self.phase+=1
        
        self.set_arrow()
        
        if you_died>0:

            messagebox.showwarning("You Died","被弾!!!!")
            self.all_reset()
        
    def button_visual_reset(self):
        col,row = self.player_current[0],self.player_current[1]
        player_pos = col + row*5
        for i in range(25):
            if i == player_pos:
                color="#0ff"
            elif i == self.goal_num:
                color="#0f0"
            elif i%2==0:
                color ="#fff"
            else:
                color="#888"
            button = self.grid_list[i]
            button["bg"] = color
            button["text"] = ("ゴール" if i==self.goal_num else "")
            button["borderwidth"] = 3
        
        
    def attack_effect(self,enemy_id):
        """
        敵の攻撃範囲の
        ボタンの色塗りをする
        """
        attack_position = self.enemy_attack_position[enemy_id]
        you_died=0 # 死亡フラグ
        col,row = self.player_current[0],self.player_current[1]
        player_pos = col + row*5
        
        for i,button in enumerate(self.grid_list):
            if i == player_pos:
                color="#0ff"
            elif i == self.goal_num:
                color="#0f0"
            elif i%2==0:
                color ="#f88"
            else:
                color="#f00"            
            if (enemy_id in ["n","s"]) and (i%5 == attack_position) or \
                (enemy_id in ["e","w"]) and (i//5 == attack_position):
                button["borderwidth"] = 5
                button["text"]="X"
                button["bg"] = color
                
                col = i%5
                row = i//5
                
                if (self.player_current[0] == col) and (self.player_current[1] == row):
                    you_died +=1
        
        return you_died
            
        
if __name__ =="__main__":
    root = tk.Tk()
    app = Application(master=root)
    app.mainloop()