from pathlib import Path

import fire
from matplotlib import pyplot as plt

from .generate_qa import draw_detections, extract_frame_info, extract_kart_objects, extract_track_info, extract_field_id


def generate_caption(info_path: str, view_index: int, img_width: int = 150, img_height: int = 100) -> list:
    """
    Generate caption for a specific view.
    """
    import os
    # Rebuild image file name
    # taken from check_qa_pairs method
    info_pth = Path(info_path)
    base_name = info_pth.stem.replace("_info", "")
    image_file = f"{base_name}_{view_index:02d}_im.jpg"
    relative_dir = info_pth.parent.relative_to("data") #probably don't need this if using ../data
    image_file = str(os.path.join(relative_dir,image_file))

    caption_pairs = []
    karts_info = extract_kart_objects(info_path,view_index,img_width,img_height)
    track = extract_track_info(info_path)
    if not karts_info:
        caption_pairs.append({
            "image_file" : image_file,
            "caption" : f"The track is {track}."
        })
        return caption_pairs

    # find center kart
    ego_kart = next((kart for kart in karts_info if kart["is_center_kart"]), None)
    # 1. Ego car
    # {kart_name} is the ego car.
    caption_pairs.append({
        "image_file" : image_file,
        "caption" : f"{ego_kart["kart_name"]} is the ego car."
    })
    # 2. Counting
    # There are {num_karts} karts in the scenario. all_mc_qas.json uses scene, not scenario
    caption_pairs.append({
        "image_file" : image_file,
        "caption" : f'There are {len(karts_info)} karts in the scene.'
    })
    # 3. Track name
    # The track is {track_name}.
    caption_pairs.append({
        "image_file" : image_file,
        "caption" : f"The track is {track}."
    })

    # 4. Relative position
    # {kart_name} is {position} of the ego car.
    ego_x, ego_y = ego_kart["center"]
    for kart in karts_info:
        if kart == ego_kart:
            continue
        kart_x, kart_y = kart["center"]
        #check left or right
        l_or_r = "left" if kart_x <= ego_x else "right"
        fr_or_bk = "front" if kart_y < ego_y else "behind"
        caption_pairs.append({
            "image_file": image_file,
            "caption": f"{kart["kart_name"]} is {l_or_r} of the ego car."
        })
        if fr_or_bk == "front":
            caption = f'{kart["kart_name"]} is in {fr_or_bk} of the ego car.'
        else:
            caption = f'{kart["kart_name"]} is {fr_or_bk} the ego car.'
        caption_pairs.append({
            "image_file": image_file,
            "caption": caption
        })

    return caption_pairs

def generate_all_captions(info_path:str, output_json:str, img_width:int = 150, img_height:int = 100):
    """
        Generate json output file for all data
        Args:
            info_path: Path to the info.json files (directory only)
            output_json: Filename for the output json file
            img_width: image width for scaling
            img_height: image height for scaling

        Returns:
            creates a json file of caption pairs
        """
    import glob
    import os, json
    # count = 0
    #all_captions = [] #comment out after valid test against golden
    for filepath in glob.glob(os.path.join(info_path, '*info.json')):
        # filepath is a json file per field id in directory provided
        # count += 1 #temp to restrict running the entire thing
        # if count > 10:
        #    break
        all_captions = [] #uncomment out after valid test against golden
        for view in range(10):
            caption_pair = generate_caption(filepath, view, img_width, img_height)
            if caption_pair:
                all_captions.extend(caption_pair)

        # save to json file
        field_id = extract_field_id(filepath)
        output_filename = info_path + field_id + output_json
        #output_filename = info_path + output_json #comment out after valid test against golden
        with open(output_filename, "w") as f:   #indent this in after valid test against golden
            json.dump(all_captions, f, indent=2)

def check_caption(info_file: str, view_index: int):
    captions = generate_caption(info_file, view_index)

    print("\nCaption:")
    print("-" * 50)
    for i, caption in enumerate(captions):
        print(f"{i + 1}. {caption}")
        print("-" * 50)

    info_path = Path(info_file)
    base_name = info_path.stem.replace("_info", "")
    image_file = list(info_path.parent.glob(f"{base_name}_{view_index:02d}_im.jpg"))[0]

    annotated_image = draw_detections(str(image_file), info_file)

    plt.figure(figsize=(12, 8))
    plt.imshow(annotated_image)
    plt.axis("off")
    plt.title(f"Frame {extract_frame_info(str(image_file))[0]}, View {view_index}")
    plt.show()


"""
Usage Example: Visualize QA pairs for a specific file and view:
   python generate_captions.py check --info_file ../data/valid/00000_info.json --view_index 0

You probably need to add additional commands to Fire below.
"""


def main():
    fire.Fire({"check": check_caption, "generate" : generate_caption, "generate_all": generate_all_captions})


if __name__ == "__main__":
    main()
