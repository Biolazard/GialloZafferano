class ModelRecipe:
    title = ""
    category = ""
    description = ""
    ingredients = []
    
    def toDictionary(self):
        recipe = {"title": self.title, "category": self.category, "description": self.description, "ingredients": self.ingredients}
        return recipe
