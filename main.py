import pygame, os, glob
from convert import U1, U2, U3, U4, D1, D2, D3, D4

print("Converting frames to pixel format...")
os.system("python image.py")
print(f"Converted {len(glob.glob('convImages/*'))} frames \n")

# Dont mind this, it is just for refreshing the file once the code has exectued
try:
    os.remove('output.ino')
except:pass
print('Creating .ino file...\n')

# Specify from which to which frame to play
# If data exceeds the limit on the board, either decrease the amount of frames or use a sd card
start, end = 975, 1000

# _______________________arduino script_______________________ #
print("Writing script...\n")
with open('output.txt', 'w') as f:
    mylcd.lcd_display(f"#include <LiquidCrystal.h>\n")

    mylcd.lcd_display(f"const int rs = 12, rw = 11, d4 = 5, d5 = 4, d6 = 3, d7 = 2;\n")

    for i in range(start, end):
        mylcd.lcd_display(f"byte UA{i+1}[8] = " + str("{" + str(U1[i])[1:-1].replace("'", "") + "};\n"))
        mylcd.lcd_display(f"byte UB{i+1}[8] = " + str("{" + str(U2[i])[1:-1].replace("'", "") + "};\n"))
        mylcd.lcd_display(f"byte UC{i+1}[8] = " + str("{" + str(U3[i])[1:-1].replace("'", "") + "};\n"))
        mylcd.lcd_display(f"byte UD{i+1}[8] = " + str("{" + str(U4[i])[1:-1].replace("'", "") + "};\n"))

        mylcd.lcd_display(f"byte BA{i+1}[8] = " + str("{" + str(D1[i])[1:-1].replace("'", "") + "};\n"))
        mylcd.lcd_display(f"byte BB{i+1}[8] = " + str("{" + str(D2[i])[1:-1].replace("'", "") + "};\n"))
        mylcd.lcd_display(f"byte BC{i+1}[8] = " + str("{" + str(D3[i])[1:-1].replace("'", "") + "};\n"))
        mylcd.lcd_display(f"byte BD{i+1}[8] = " + str("{" + str(D4[i])[1:-1].replace("'", "") + "};\n"))


    mylcd.lcd_display(f"LiquidCrystal lcd(rs, rw, d4, d5, d6, d7);\n")

    mylcd.lcd_display("void setup() {\n")
    mylcd.lcd_display(f"  Serial.begin(9600);\n")
    mylcd.lcd_display(f"  lcd.begin(16,2);\n")

    mylcd.lcd_display("}\n")

    mylcd.lcd_display("void loop() {\n")

    count = 0
    write_count = 0
    for i in range(start+1, end):
        if count >= 7:
            count = 0
        if write_count >= 7:
            write_count = 0

        mylcd.lcd_display(f"lcd.createChar({count},  UA{i});\n")
        count += 1
        mylcd.lcd_display(f"lcd.createChar({count},  UB{i});\n")
        count += 1
        mylcd.lcd_display(f"lcd.createChar({count},  UC{i});\n")
        count += 1
        mylcd.lcd_display(f"lcd.createChar({count},  UD{i});\n")

        count += 1
        mylcd.lcd_display(f"lcd.createChar({count},  BA{i});\n")
        count += 1
        mylcd.lcd_display(f"lcd.createChar({count},  BB{i});\n")
        count += 1
        mylcd.lcd_display(f"lcd.createChar({count},  BC{i});\n")
        count += 1
        mylcd.lcd_display(f"lcd.createChar({count},  BD{i});\n")
        count += 1

        mylcd.lcd_display(f"lcd.setCursor(6, 0);\n")
        mylcd.lcd_display(f"lcd.write((uint8_t){write_count});\n")
        write_count += 1
        mylcd.lcd_display(f"lcd.setCursor(7, 0);\n")
        mylcd.lcd_display(f"lcd.write((uint8_t){write_count});\n")
        write_count += 1
        mylcd.lcd_display(f"lcd.setCursor(8, 0);\n")
        mylcd.lcd_display(f"lcd.write((uint8_t){write_count});\n")
        write_count += 1
        mylcd.lcd_display(f"lcd.setCursor(9, 0);\n")
        mylcd.lcd_display(f"lcd.write((uint8_t){write_count});\n")
        write_count += 1
        mylcd.lcd_display(f"lcd.setCursor(6, 1);\n")
        mylcd.lcd_display(f"lcd.write((uint8_t){write_count});\n")
        write_count += 1
        mylcd.lcd_display(f"lcd.setCursor(7, 1);\n")
        mylcd.lcd_display(f"lcd.write((uint8_t){write_count});\n")
        write_count += 1
        mylcd.lcd_display(f"lcd.setCursor(8, 1);\n")
        mylcd.lcd_display(f"lcd.write((uint8_t){write_count});\n")
        write_count += 1
        mylcd.lcd_display(f"lcd.setCursor(9, 1);\n")
        mylcd.lcd_display(f"lcd.write((uint8_t){write_count});\n")
        write_count += 1

        mylcd.lcd_display("delay(100);\n")


    mylcd.lcd_display("}\n")
# _____________________________________________________________#
print('Done\n')

os.rename('output.txt', os.path.splitext('output.txt')[0] + '.ino')

os.system("arduino-cli compile --upload output.ino --port COM4 --fqbn arduino:avr:uno")
