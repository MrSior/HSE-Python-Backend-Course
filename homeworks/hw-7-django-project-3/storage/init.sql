TRUNCATE TABLE blog_like CASCADE;
TRUNCATE TABLE blog_comment CASCADE;
TRUNCATE TABLE blog_post CASCADE;
TRUNCATE TABLE blog_user RESTART IDENTITY CASCADE;

INSERT INTO blog_user (username, email, password, is_superuser, is_staff, is_active, date_joined, first_name, last_name)
VALUES 
    ('user1', 'user1@example.com', 'password1', FALSE, FALSE, TRUE, NOW(), 'User1', 'Last1'),
    ('user2', 'user2@example.com', 'password2', FALSE, FALSE, TRUE, NOW(), 'User2', 'Last2');

INSERT INTO blog_post (title, content, author_id, created_at)
VALUES 
    ('First Post', 'Content of the first post', 1, NOW()),
    ('Second Post', 'Content of the second post', 2, NOW());

INSERT INTO blog_comment (post_id, author_id, content, created_at)
VALUES 
    (1, 2, 'First comment on first post', NOW()),
    (2, 1, 'First comment on second post', NOW());

INSERT INTO blog_like (user_id, post_id, comment_id)
VALUES 
    (1, 1, NULL),  -- Лайк от user1 на post1
    (2, 2, NULL);  -- Лайк от user2 на post2

INSERT INTO blog_like (user_id, post_id, comment_id)
VALUES 
    (1, NULL, 1),  -- Лайк от user1 на comment1
    (2, NULL, 2);  -- Лайк от user2 на comment2