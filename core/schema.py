import graphene
from graphene_django import DjangoObjectType
from books.models import Books


class BookType(DjangoObjectType):
    class Meta:
        model = Books
        fields = ("id", "title", "description")

class CreateBookMutation(graphene.Mutation):
    class Argument:
        title = graphene.String()
        description = graphene.String()

    def mutate(self, info, title, description):
        book = Books(title=title, description=description)
        book.save()
        return CreateBookMutation(book=book)

class DeleteBookMutation(graphene.Mutation):
    class  Arguments:
        id = graphene.ID(required=True)

    message = graphene.String()

    def mutate(self, info, id):
        book = Books.objects.get(pk=id)
        book.delete()
        return DeleteBookMutation(message="Book deleted")

class UpdateBookMutation(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)
        title = graphene.String()
        description = graphene.String()

    book = graphene.Field(BookType)

    def mutate(self, info, id, title, description):
        book = Books.objects.get(pk=id)
        book.title = title
        book.description = description
        book.save()
        return  UpdateBookMutation (book=book)

class Query(graphene.ObjectType):
    hello = graphene.String(default_value="Hello!")
    books = graphene.List(BookType)
    book = graphene.Field(BookType, id=graphene.ID())

    def resolve_books(self, info):
        return Books.objects.all()

    def resolve_book(self, info, id):
        return Books.objects.all(pk=id)

class Mutation(graphene.ObjectType):
    create_book = CreateBookMutation.Field()
    delete_book = DeleteBookMutation.Field()
    update_book = UpdateBookMutation.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)
