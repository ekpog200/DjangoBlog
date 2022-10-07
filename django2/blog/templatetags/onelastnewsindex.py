from django import template
from blog.models import Post

register = template.Library()

@register.inclusion_tag('blog/onelastnewsindex.html')
def onelastnewsindex():
    try:
        content = Post.objects.get(news_day=True)
    except:
        content = Post.objects.latest('pk')
    return {'content': content}
