from django.conf.urls.defaults import *
from hashtags.models import Hashtag
from hashtags.views import hashtag_index, hashtagged_item_list

index_url = url(
    regex  = '^$',
    view   = hashtag_index,
    name   = 'hashtag_index',
)

hashtagged_item_list_url = url(
    regex  = '^(?P<hashtag>[-\w]+)/$',
    view   = hashtagged_item_list,
    name   = 'hashtagged_item_list'
)

urlpatterns = patterns('', index_url, hashtagged_item_list_url)
