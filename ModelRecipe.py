class ModelRecipe:
    title = ""
    category = ""
    description = ""
    ingredients = []
    
    def toDictionary(self):
        recipe = {"title": self.title, "category": self.category, "ingredients": self.ingredients, "description": self.description}
        return recipe
