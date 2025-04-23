import json
import os
from datetime import datetime

class Author:
    def __init__(self, name: str, email: str):
        self.__name = name
        self.__email = email
        self.__articles = []

    @property
    def name(self):
        return self.__name

    @property
    def email(self):
        return self.__email

    def add_article(self, article):
        self.__articles.append(article)

    def get_articles(self):
        return self.__articles

    def __str__(self):
        return f"Author: {self.__name} ({self.__email})"

class Category:
    def __init__(self, name: str):
        self.__name = name
        self.__articles = []

    @property
    def name(self):
        return self.__name

    def add_article(self, article):
        self.__articles.append(article)

    def get_articles(self):
        return self.__articles

    def __str__(self):
        return f"Category: {self.__name}"

class Article:
    def __init__(self, title: str, content: str, author: Author, category: Category):
        self.__title = title
        self.__content = content
        self.__author = author
        self.__category = category
        self.__published_at = None

        author.add_article(self)
        category.add_article(self)

    @property
    def title(self):
        return self.__title

    @property
    def content(self):
        return self.__content

    @property
    def author(self):
        return self.__author

    @property
    def category(self):
        return self.__category

    @property
    def published_at(self):
        return self.__published_at

    def edit(self, new_title: str, new_content: str):
        self.__title = new_title
        self.__content = new_content

    def publish(self):
        self.__published_at = datetime.now()

    def __str__(self):
        return f"Article: {self.__title} by {self.__author.name} in {self.__category.name}" + (f" (Published: {self.__published_at})" if self.__published_at else " (Draft)")

# FACTORY METHODS
class EntityFactory:
    @staticmethod
    def get_or_create_author(name: str, email: str, authors: dict):
        if email in authors:
            return authors[email]
        author = Author(name, email)
        authors[email] = author
        return author

    @staticmethod
    def get_or_create_category(name: str, categories: dict):
        if name in categories:
            return categories[name]
        category = Category(name)
        categories[name] = category
        return category

class ArticleFactory:
    @staticmethod
    def create_article(title: str, content: str, author: Author, category: Category, publish: bool = True) -> Article:
        article = Article(title, content, author, category)
        if publish:
            article.publish()
        return article

def load_from_json(filename="database.json"):
    try:
        with open(filename, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {"authors": [], "categories": [], "articles": []}

def save_to_json(data, filename="database.json"):
    with open(filename, "w") as file:
        json.dump(data, file, indent=4)

def show_data(data):
    print("=== CATÁLOGO ===\n\n")

    print("🧠 Autores 🧠\n")
    for author in data.get("authors", []):
        print(f"- {author['name']} ({author['email']})")

    print("\n📁 Categorias 📁\n")
    for category in data.get("categories", []):
        print(f"- {category['name']}")
        
    print("\n📝 Artigos 📝\n")
    for article in data.get("articles", []):
        print(f"- \"{article['title']}\" por {article['author']} em {article['category']} ({article['published_at']})")
    
def exibir_artigo(data):
    artigos = data.get("articles", [])
    
    if not artigos:
        print("Nenhum artigo cadastrado.")
        return

    print("=== LISTA DE ARTIGOS ===")
    for i, artigo in enumerate(artigos, start=1):
        print(f"{i}. {artigo['title']} (por {artigo['author']})")

    try:
        escolha = int(input("\nDigite o número do artigo que deseja ver o conteúdo:\n"))
        if 1 <= escolha <= len(artigos):
            artigo = artigos[escolha - 1]
            os.system('cls')
            print("=== ARTIGO SELECIONADO ===")
            print(f"Título: {artigo['title']}")
            print(f"Autor: {artigo['author']}")
            print(f"Categoria: {artigo['category']}")
            print(f"Publicado em: {artigo['published_at']}")
            print("\nConteúdo:")
            print(artigo['content'])
        else:
            print("Número inválido.")
    except ValueError:
        print("Entrada inválida. Por favor, digite um número.")



def main():
    user_input = ''
    user_input_return = ''

    while(user_input != '3'):

        os.system('cls')
        print("=== MENU PRINCIPAL ===\n")

        data = load_from_json()
        authors = {author["email"]: Author(author["name"], author["email"]) for author in data.get("authors", [])}
        categories = {cat["name"]: Category(cat["name"]) for cat in data.get("categories", [])}


        print('1. Ver Catalogo')
        print("2. Adicionar um novo Artigo")
        print("3. Encerrar o programa")
        
        user_input = input('\n')
    
        if user_input == '1':

            

            while(user_input_return != '2' ):

                os.system('cls')
                show_data(data)
                print('\n')

                print("1. Ver conteudo dos artigos")
                print("2. Retornar paro o Menu Principal")
                print("3. Encerrar o programa")

                user_input_return = input('\n')

                if user_input_return == '1' :
                    os.system('cls') 
                    exibir_artigo(data)
                    
                    print('\nDigite 0 para retornar.')
                    while(user_input_return != '0'):
                        user_input_return = input('')
                        os.system('cls')

                elif user_input_return == '3': os.abort()

            user_input_return = 0


        elif user_input == '2':

            name = input("Digite o nome do autor: ")
            email = input("Digite o email do autor: ")
            author = EntityFactory.get_or_create_author(name, email, authors)

            category_name = input("Digite o nome da categoria: ")
            category = EntityFactory.get_or_create_category(category_name, categories)

            title = input("Digite o título do artigo: ")
            content = input("Digite o conteúdo do artigo: ")

            article = ArticleFactory.create_article(title, content, author, category)

            if not any(a["email"] == author.email for a in data["authors"]):
                data["authors"].append({"name": author.name, "email": author.email})

            if not any(c["name"] == category.name for c in data["categories"]):
                data["categories"].append({"name": category.name})

            data["articles"].append({
                "title": article.title,
                "content": article.content,
                "author": author.email,
                "category": category.name,
                "published_at": article.published_at.strftime("%Y-%m-%d %H:%M:%S")
            })

            save_to_json(data)
            os.system('cls')
            print("Artigo salvo com sucesso!")
            while(user_input_return != '1'):
                user_input_return = input('Digite 1 para retornar para o menu principal ou 2 para encerrar o programa.\n')
                if user_input_return == '2': os.abort()
            user_input_return = 0


if __name__ == "__main__":
    main()
