def filter_comments_by_author(comments, author):
    res = []
    for comment in comments:
        if comment.author_id == author.id:
            res.append(comment)

    return res
