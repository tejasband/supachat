-- SupaChat Database Schema

-- Articles Table
CREATE TABLE IF NOT EXISTS articles (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    topic VARCHAR(100) NOT NULL,
    author VARCHAR(100) NOT NULL,
    publish_date DATE NOT NULL
);

-- Pageviews Table
CREATE TABLE IF NOT EXISTS pageviews (
    id SERIAL PRIMARY KEY,
    article_id INTEGER REFERENCES articles(id),
    viewed_at TIMESTAMP NOT NULL,
    visitor_id VARCHAR(100)
);

-- Engagement Table
CREATE TABLE IF NOT EXISTS engagement (
    id SERIAL PRIMARY KEY,
    article_id INTEGER REFERENCES articles(id),
    action_type VARCHAR(50) NOT NULL, -- e.g., 'like', 'share', 'comment'
    created_at TIMESTAMP NOT NULL
);

-- Seed Data (Simulating Analytics over the last 30 days)
INSERT INTO articles (title, topic, author, publish_date) VALUES 
('The Rise of AI in 2024', 'AI', 'Alice Smith', CURRENT_DATE - INTERVAL '25 days'),
('Dockerize Everything', 'DevOps', 'Bob Jones', CURRENT_DATE - INTERVAL '20 days'),
('Next.js Performance Tips', 'Frontend', 'Charlie Day', CURRENT_DATE - INTERVAL '15 days'),
('Why MCP is the Future', 'AI', 'Alice Smith', CURRENT_DATE - INTERVAL '10 days'),
('Building a Chatbot in React', 'Frontend', 'Daisy Lee', CURRENT_DATE - INTERVAL '5 days');

-- Seed Pageviews
DO $$
DECLARE
    art_id INT;
    v_date TIMESTAMP;
BEGIN
    FOR i IN 1..300 LOOP -- 300 random pageviews
        art_id := floor(random() * 5 + 1);
        v_date := CURRENT_TIMESTAMP - (random() * 30 * interval '1 day');
        INSERT INTO pageviews (article_id, viewed_at, visitor_id) 
        VALUES (art_id, v_date, 'visitor_' || floor(random() * 100));
    END LOOP;
END $$;

-- Seed Engagement
DO $$
DECLARE
    art_id INT;
    action VARCHAR(50);
    actions VARCHAR ARRAY := ARRAY['like', 'share', 'comment'];
    v_date TIMESTAMP;
BEGIN
    FOR i IN 1..100 LOOP -- 100 random engagements
        art_id := floor(random() * 5 + 1);
        action := actions[floor(random() * 3 + 1)];
        v_date := CURRENT_TIMESTAMP - (random() * 30 * interval '1 day');
        INSERT INTO engagement (article_id, action_type, created_at) 
        VALUES (art_id, action, v_date);
    END LOOP;
END $$;
