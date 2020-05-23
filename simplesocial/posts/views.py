from django.shortcuts import render

# ############################## POSTS APP VIEWS ########################
# Importing CBV Mixins
from django.contrib.auth.mixins import LoginRequiredMixin

from django.urls import reverse_lazy

# to display a one-time notification message (also known as “flash message”) to the user after processing a form
# or some other types of user input.
from django.contrib import messages
# The general CBVs
from django.views import generic

# to raise 404 error
from django.http import Http404

# Extra methods required to insure that certain privileges are connected to
# the logged-in user and selected Group!
# need django-braces(pip install django-braces), allows to access some convenient Mixins to use with CBVs
from braces.views import SelectRelatedMixin

from . import models
from . import forms

from django.contrib.auth import get_user_model
User = get_user_model()

# PostListView(simple view), by selecting a person one can see all their posts/ or a group to
# see all the posts in that particular Group

class PostList(SelectRelatedMixin, generic.ListView):
    """
    List view of all posts connected to Post model,
    the 'select_related' (mixin) gives a tuple of current user and selected group
    """
    model = models.Post
    # mixin provides a tuple of related models(User and Group are foreign key related to model Posts)
    # i.e., the user and the group the current post belongs to
    select_related = ('user', 'group')

class UserPosts(generic.ListView):
    """
    The view of all posts by user
    """
    model = models.Post
    template_name = 'posts/user_post_list.html'

    def get_queryset(self):
        """
        the queryset (ORM)(perform SQLqueries in django),
        try to set,
        set the current user(ie user belongs to this particular post(self.post.user) equals to
        the username exactly equal to the current username(by using 'get')
        when one call the queryset at the userpost, if the user exists, it fetch all the posts
        related to the user using the iexact
        :return:
        """
        try:
            self.post_user = User.objects.prefetch_related('posts').get(username__iexact=self.kwargs.get('username'))
        except User.DoesNotExist:
            # if user deleted or not exists
            raise Http404
        else:
            return self.post_user.posts.all()

    # get_context_data is used to give extra information rather than the generic CBVs
    # It is used to override default views to send more.
    def get_context_data(self, **kwargs):
        """
        grab the 'post_user'
        returning posts context data to the user
        :param kwargs:
        :return:
        """
        # super is used to find the "parent class" and return its object, i.e, in get_context_data function inherits
        # from parent(ie self).That means get_context_data inherits all functions from parent class.
        # If one choose to call super, he is calling the Parent's function together with your own implementation.
        # simply, one can use parents attributes and methods mixed with his own.

        # here super() + Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # modifying the context with post_user/Add in a QuerySet of post_user
        context['post_user'] = self.post_user
        return context

class PostDetail(SelectRelatedMixin, generic.DetailView):
    """
    Post Detailed View
    """
    model = models.Post
    select_related = ('user', 'group')

    def get_queryset(self):
        """
        DB queries to filter the post list with only user as auther
        :return:
        """
        # Get the queryset for the actual post
        queryset = super().get_queryset()
        # Filter the username of posts that matches exactly with the current user's username
        return queryset.filter(user__username__iexact=self.kwargs.get('username'))

# ### Need to Create The CreatePost & DeletePost views as to CRUD--> data management

class CreatePost(LoginRequiredMixin, SelectRelatedMixin, generic.CreateView):
    """
    View to create a Post in a particular Group
    """
    # Editable fields
    fields = ('message', 'group')
    model = models.Post

    def form_valid(self, form):
        """
        To find form valid or not
        :param form:
        :return:
        """
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return super().form_valid(form)

class DeletePost(LoginRequiredMixin, SelectRelatedMixin, generic.DeleteView):
    """
    View to Delete a Post
    """
    model = models.Post
    select_related = ('user', 'group')
    # After delete go back to all the posts
    success_url = reverse_lazy('posts:all')

    def get_queryset(self):
        """
        get_queryset to add logic to the queryset selection.
        :return: filtered ot the contents with current user id
        """
        # super represents parent model ie Posts,
        # get_queryset on Posts
        queryset = super().get_queryset()
        # self.request.user to filter using the current user
        return queryset.filter(user_id=self.request.user.id)

    def delete(self, *args, **kwargs):
        """
        messeges that Post deleted using inbuilt messages framework
        :param args:
        :param kwargs:
        :return:
        """
        # 'messages.success' is used when an action was successful, here “Post Deleted”
        messages.success(self.request, 'Post Deleted')
        return super().delete(*args, **kwargs)