# rblike Extension for Review Board.

from __future__ import unicode_literals

from django.conf import settings
from django.conf.urls import patterns, include
from reviewboard.extensions.base import Extension, JSExtension
from reviewboard.extensions.hooks import CommentDetailDisplayHook
from reviewboard.urls import reviewable_url_names, review_request_url_names

apply_to_url_names = set(reviewable_url_names + review_request_url_names)


class LikeCommentDetailDisplay(CommentDetailDisplayHook):
    HTML_EMAIL_COMMON_SEVERITY_CSS = (
        'font-weight: bold;'
        'font-size: 9pt;'
    )

    HTML_EMAIL_SPECIFIC_SEVERITY_CSS = {
        'like': 'color: green;'
    }

    def render_review_comment_detail(self, comment):
        """Renders the number of like of a comment on a review."""
        like = comment.extra_data.get('like')

        if not like:
            return ''

        return ('<p class="comment-like">'
                'Like: %s'
                '</p>'
                % like)

    def render_email_comment_detail(self, comment, is_html):
        """Renders the like of a comment on an e-mail."""
        like = comment.extra_data.get('like')

        if not like:
            return ''

        if is_html:
            specific_css = self.HTML_EMAIL_SPECIFIC_SEVERITY_CSS.get('like', '')

            return ('<p style="%s%s">Like: %s</p>'
                    % (self.HTML_EMAIL_COMMON_SEVERITY_CSS,
                       specific_css, like))
        else:
            return 'Like: %s\n' % like


class LikeJSExtension(JSExtension):
    model_class = 'RBLIKE.Extension'
    apply_to = apply_to_url_names


class RBLike(Extension):
    metadata = {
        'Name': 'rblike',
        'Summary': 'Add like button to reviewboard.',
    }

    js_extensions = [LikeJSExtension]

    js_bundles = {
        'default': {
            'source_filenames': ['js/rbLike.js'],
            'apply_to': apply_to_url_names,
        }
    }

    def initialize(self):
        LikeCommentDetailDisplay(self)
