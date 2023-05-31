import json
import os

DEBUG = True

if __name__ == "__main__":
    recipes = sorted(
        [
            os.path.join(os.getcwd(), "Recipes", recipie)
            for recipie in os.listdir("Recipes")
        ]
    )
    null_images = 0
    for recipe in recipes:
        readable_name = (
            recipe.split("/")[-1].replace(".json", "").replace("_", " ").capitalize()
        )
        if DEBUG:
            print(f"Checking {readable_name}...", end="")
        with open(recipe, "r") as recipe_file:
            json_recipe = json.load(recipe_file)
            image_does_not_exist = json_recipe["imageBase64"] is None
            null_images += int(image_does_not_exist)

            if DEBUG:
                if image_does_not_exist:
                    print("[MISSING]")
                else:
                    print("[OK!]")

    print(f"Total missing images: {null_images} / {len(recipes)}")
