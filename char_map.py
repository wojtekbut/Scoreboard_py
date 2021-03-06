
class CharMap(object):
    CH0 = ""
    CH1 = "Left mouse"
    CH2 = "Right mouse"
    CH3 = "Control-break"
    CH4 = "Middle mouse"
    CH5 = "X1 mouse"
    CH6 = "X2 mouse"
    CH8 = "BACKSPACE"
    CH9 = "TAB"
    CH12 = "CLEAR"
    CH13 = "ENTER"
    CH16 = "SHIFT"
    CH17 = "CTRL"
    CH18 = "ALT"
    CH19 = "PAUSE"
    CH20 = "CAPS"
    CH21 = "IME Kana mode"
    CH23 = "IME Junja mode"
    CH24 = "IME final mode"
    CH25 = "IME Kanji mode"
    CH27 = "ESC"
    CH28 = "IME convert"
    CH29 = "IME nonconvert"
    CH30 = "IME accept"
    CH31 = "IME mode change request"
    CH32 = "SPACEBAR"
    CH33 = "PG UP"
    CH34 = "PG DOWN"
    CH35 = "END"
    CH36 = "HOME"
    CH37 = "LEFT"
    CH38 = "UP"
    CH39 = "RIGHT"
    CH40 = "DOWN"
    CH41 = "SELECT"
    CH42 = "PRINT"
    CH43 = "EXECUTE"
    CH44 = "PRTSC"
    CH45 = "INS"
    CH46 = "DEL"
    CH47 = "HELP"
    CH48 = "0"
    CH49 = "1"
    CH50 = "2"
    CH51 = "3"
    CH52 = "4"
    CH53 = "5"
    CH54 = "6"
    CH55 = "7"
    CH56 = "8"
    CH57 = "9"
    CH65 = "A"
    CH66 = "B"
    CH67 = "C"
    CH68 = "D"
    CH69 = "E"
    CH70 = "F"
    CH71 = "G"
    CH72 = "H"
    CH73 = "I"
    CH74 = "J"
    CH75 = "K"
    CH76 = "L"
    CH77 = "M"
    CH78 = "N"
    CH79 = "O"
    CH80 = "P"
    CH81 = "Q"
    CH82 = "R"
    CH83 = "S"
    CH84 = "T"
    CH85 = "U"
    CH86 = "V"
    CH87 = "W"
    CH88 = "X"
    CH89 = "Y"
    CH90 = "Z"
    CH91 = "Lt Windows"
    CH92 = "Rt Windows"
    CH93 = "Applications"
    CH95 = "Sleep"
    CH96 = "Pad 0"
    CH97 = "Pad 1"
    CH98 = "Pad 2"
    CH99 = "Pad 3"
    CH100 = "Pad 4"
    CH101 = "Pad 5"
    CH102 = "Pad 6"
    CH103 = "Pad 7"
    CH104 = "Pad 8"
    CH105 = "Pad 9"
    CH106 = "Multiply"
    CH107 = "Add"
    CH108 = "Separator"
    CH109 = "Subtract"
    CH110 = "Decimal"
    CH111 = "Divide"
    CH112 = "F1"
    CH113 = "F2"
    CH114 = "F3"
    CH115 = "F4"
    CH116 = "F5"
    CH117 = "F6"
    CH118 = "F7"
    CH119 = "F8"
    CH120 = "F9"
    CH121 = "F10"
    CH122 = "F11"
    CH123 = "F12"
    CH124 = "F13"
    CH125 = "F14"
    CH126 = "F15"
    CH127 = "F16"
    CH128 = "F17"
    CH129 = "F18"
    CH130 = "F19"
    CH131 = "F20"
    CH132 = "F21"
    CH133 = "F22"
    CH134 = "F23"
    CH135 = "F24"
    CH144 = "NUM LOCK"
    CH145 = "SCRLK"
    CH160 = "Left SHIFT"
    CH161 = "Right SHIFT"
    CH162 = "Left CONTROL"
    CH163 = "Right CONTROL"
    CH164 = "Left MENU"
    CH165 = "Right MENU"
    CH166 = "Browser Back"
    CH167 = "Browser Forward"
    CH168 = "Browser Refresh"
    CH169 = "Browser Stop"
    CH170 = "Browser Search"
    CH171 = "Browser Favorites"
    CH172 = "Browser Start and Home"
    CH173 = "Volume Mute"
    CH174 = "Volume Down"
    CH175 = "Volume Up"
    CH176 = "Next Track"
    CH177 = "Previous Track"
    CH178 = "Stop Media"
    CH179 = "Play/Pause Media"
    CH180 = "Start Mail"
    CH181 = "Select Media"
    CH182 = "Start Application 1"
    CH183 = "Start Application 2"
    CH186 = "';CH ='"
    CH187 = "'+'"
    CH188 = "','"
    CH189 = "'-'"
    CH190 = "'.'"
    CH191 = "'/?'"
    CH192 = "'`~'"
    CH219 = "'[{'"
    CH220 = "'\\|'"
    CH221 = "']}'"
    CH222 = "sgl/dbl-quote"
    CH226 = "angle bracket or the backslash"
    CH229 = "IME PROCESS"
    CH246 = "Attn"
    CH247 = "CrSel"
    CH248 = "ExSel"
    CH249 = "Erase EOF"
    CH250 = "Play"
    CH251 = "Zoom"
    CH253 = "PA1"
    CH254 = "Clear"


    @staticmethod
    def get(num):
        naz = "CH"+str(num)
        return getattr(CharMap, naz, "ERROR! Try again!")



