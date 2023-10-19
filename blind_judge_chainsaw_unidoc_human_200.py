import os
import random
import csv

import matplotlib.pyplot as plt
import matplotlib.image as mpimg

def read_existing_decisions(csv_file):
    if not os.path.exists(csv_file):
        return {}
    with open(csv_file, mode='r') as file:
        reader = csv.reader(file)
        return {rows[0]: rows[1] for rows in reader}
def judge_image(chain_id, img_dir):
    """
    Display the combined image for a given chain_id and prompt the user
    for judgment. Returns the user's judgment (1, 2, or 0) and the method
    that was displayed on top.
    """
    img_path = os.path.join(img_dir, chain_id + '_combined.png')
    # open the image using matplotlib
    plt.figure(figsize=(15, 10))
    imgplot = plt.imshow(mpimg.imread(img_path))
    plt.axis('off')
    plt.tight_layout()
    plt.ion()
    plt.show()
    # Open the image using the default viewer
    # os.system(f"open {img_path}")
    print("Please evaluate the image:")
    print("Enter 1 if the first row is better.")
    print("Enter 2 if the second row is better.")
    print("Enter 0 if both rows are equal.")
    judgement = int(input("Your input: "))
    while judgement not in [0, 1, 2]:
        print("Invalid input. Please enter 0, 1, or 2.")
        judgement = int(input("Your input: "))
    plt.close()
    return judgement

def log_results(chain_id, methods, judgement, csv_file):
    """
    Append the results to a CSV file.
    """
    best_method_lookup = {1:methods[0], 2:methods[1], 0:'equal'}
    best_method = best_method_lookup[judgement]
    with open(csv_file, 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([chain_id, best_method, int(best_method=='chainsaw'), int(best_method=='unidoc'), int(best_method=='equal')])

def judge_images(image_dir):
    csv_path = os.path.join('..', "judgements.csv")
    decisions = read_existing_decisions(csv_path)
    image_files = [f for f in os.listdir(image_dir) if f.endswith('.png')]
    for f in image_files:
        chain_id = f.split('_combined.png')[0]
        if chain_id in decisions:
            continue
        if sum(ord(c) for c in chain_id) % 2 == 0: # randomly decide which method should be on top based on hash
            methods = ['chainsaw', 'unidoc']
        else:
            methods = ['unidoc', 'chainsaw']
        print(methods)
        # Prompt user for judgment
        judgement = judge_image(chain_id, image_dir)

        # If the file doesn't exist, create it and write the headers
        if not os.path.exists(csv_path):
            with open(csv_path, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(['Chain_ID', 'Top_Method', 'Chainsaw_Better', 'Unidoc_Better', 'Equal'])
        log_results(chain_id, methods, judgement, csv_path)



if __name__=="__main__":
    image_dir = "../chainsaw_vs_unidoc_human_200_images"
    judge_images(image_dir)