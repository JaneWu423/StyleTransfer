import os
import subprocess

count = 0

# abstract expressionism
abstract_folder = 'wikiart/training_images/Abstract_Expressionism'
file_path = 'wikiart/training_images/Abstract_Expressionism/aaron-siskind_acolman-1-1955.jpg'
for f in os.listdir(abstract_folder):
    count += 1
    file_path = os.path.join(abstract_folder, f).replace("\\", "/")
    subprocess.run(["python", "test_mult.py", "--name", "styleMixer_bw1_style3.00_cont3.00_iden1.00_cx3.00_1", 
                "--style", file_path, 
                "--content", "wikiart/content_image/c1.jpg"])
    print(count)


# ukiyoe
ukiyoe_folder = 'wikiart/training_images/Ukiyo_e'
for f in os.listdir(ukiyoe_folder):
    file_path = os.path.join(ukiyoe_folder, f).replace("\\", "/")
    subprocess.run(["python", "test_mult.py", "--name", "styleMixer_bw1_style3.00_cont3.00_iden1.00_cx3.00_1", 
                "--style", file_path, 
                "--content", "wikiart/content_image/c1.jpg",
                "--output", "./wikiart/generated/Ukiyo_e"])
    count += 1
    print(count)



# realism
realism_folder = 'wikiart/training_images/Realism'
for f in os.listdir(realism_folder):
    file_path = os.path.join(realism_folder, f).replace("\\", "/")
    subprocess.run(["python", "test_mult.py", "--name", "styleMixer_bw1_style3.00_cont3.00_iden1.00_cx3.00_1", 
                "--style", file_path, 
                "--content", "wikiart/content_image/c1.jpg",
                "--output", "./wikiart/generated/Realism"])
    count += 1
    print(count)