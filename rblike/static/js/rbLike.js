//commentDialogView.js
//render function is called and allowed to hook any new js class

//distribution:
//1. python setup.py bdist_egg
//2. easy_install dist/rblike-0.1-py2.7.egg

RBLIKE = {}



RBLIKE.CommentDialogHookView = Backbone.View.extend({
    events: {
        'click .buttons .save-like': '_saveLike'
    },

    buttonsTemplate: _.template([
        '<span class="like-action">',
        '  <input type="button" class="save-like" value="Like" disabled="true" />',
        '</span>'
    ].join('')),

    /*
     * Initializes the view.
     */
    initialize: function(options) {
        this.commentDialog = options.commentDialog;
        this.commentEditor = options.commentEditor;
        //get old like number as initialize value
        this.like = this.commentEditor.get('extraData').like;
        if(this.like === undefined){
            this.like = 0;
        }
        //caching comment purpose
        this.cachedText = '';
    },

    render : function(){
        var $likeButton = $(this.buttonsTemplate());

        //insert like button right before cancel button
        this.commentDialog.$cancelButton.before($likeButton);

        //if users can edit so they can see like button
        //if users can save comment, they can click on like button also
        $likeButton.find('input')
            .bindVisibility(this.commentEditor, 'canEdit')
            .bindProperty('disabled', this.commentEditor, 'canSave', {
                elementToModel : false,
                inverse : true
            });
    },

    _saveLike: function() {
        if(this.commentEditor.get('canSave')){
            //prevent users to continuous clicking too fast on like button
            if(this.commentEditor.get('text') !== this.cachedText){
                this.like = this.like + 1;
                this.commentEditor.setExtraData('like', this.like);
                this.commentDialog.save();
                //cache new text
                this.cachedText = this.commentEditor.get('text');
            }
        }
    }
});

RBLIKE.ReviewDialogCommentHookView = Backbone.View.extend({

});

RBLIKE.Extension = RB.Extension.extend({
    initialize: function() {
        _super(this).initialize.call(this);

        new RB.CommentDialogHook({
            extension: this,
            viewType: RBLIKE.CommentDialogHookView
        });

        new RB.ReviewDialogCommentHook({
            extension: this,
            viewType: RBLIKE.ReviewDialogCommentHookView
        });
    }
});