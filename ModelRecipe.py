class ModelRecipe:
    imageBase64 = ""
    title = ""
    category = ""
    description = ""
    ingredients = []
    
    def toDictionary(self):
        recipe = {"imageBase64": self.imageBase64, "title": self.title, "category": self.category, "description": self.description, "ingredients": self.ingredients}
        return recipe
