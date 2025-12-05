Quick Start
Prerequisites

ก่อนเริ่มใช้งาน ควรติดตั้ง:

Docker Desktop
 (รวม Docker Compose)

Node.js
 เวอร์ชัน 18 ขึ้นไป (ถ้าจะเชื่อมกับ Frontend ภายนอก)

Git

Code Editor (แนะนำ VS Code
)

⚡ เริ่มต้นใช้งาน (ประมาณ 5 นาที)

Clone Repository

git clone https://github.com/zhiwei-chen-bu/project_api.git
cd project_api


เริ่ม Backend + Database ด้วย Docker

docker-compose up -d


Docker จะทำงานดังนี้:

สร้าง MySQL container

รัน init.sql เพื่อสร้างตารางและข้อมูลตัวอย่าง

Start FastAPI server (อ่านโค้ดจากโฟลเดอร์ api/)

ตรวจสอบ API ผ่าน Swagger UI

เปิด browser ไปที่:

http://localhost:8000/docs

คุณจะเห็น Swagger UI สำหรับทดสอบ API ได้ทันที

API Endpoints
Method	Endpoint	Description	Response
GET	/	API information / endpoints list	JSON (info + endpoints)
GET	/api/word	สุ่มคำศัพท์ 1 คำ	Word object
POST	/api/validate-sentence	ตรวจประโยค + ให้คะแนนตามคำศัพท์ที่ใช้	Validation result
GET	/api/summary	สถิติการฝึกทั้งหมด	Summary statistics
GET	/api/history	ประวัติการฝึกทั้งหมด	Array of practice sessions
GET	/health	Health check	Status object

รายละเอียดพฤติกรรมจริงของแต่ละ endpoint ดูได้จากโค้ดในโฟลเดอร์ api/ และหน้า /docs

ตัวอย่างการใช้งาน API
1. ดึงคำศัพท์แบบสุ่ม

Request

curl http://localhost:8000/api/word


ตัวอย่าง Response

{
  "id": 1,
  "word": "apple",
  "definition": "A round fruit with red, green, or yellow skin",
  "difficulty_level": "Beginner"
}

2. ส่งประโยคเพื่อตรวจสอบ (Validate Sentence)

Request

curl -X POST http://localhost:8000/api/validate-sentence \
  -H "Content-Type: application/json" \
  -d '{
    "word_id": 1,
    "sentence": "I eat an apple every morning for breakfast"
  }'


ตัวอย่าง Response (Mock AI / ระบบให้คะแนนจำลอง)

{
  "score": 8.5,
  "level": "Beginner",
  "suggestion": "Excellent! Your sentence is well-structured and descriptive.",
  "corrected_sentence": "I eat an apple every morning for breakfast"
}

3. ดูสถิติการฝึก (Summary)

Request

curl http://localhost:8000/api/summary


ตัวอย่าง Response

{
  "total_practices": 15,
  "average_score": 7.8,
  "total_words_practiced": 5,
  "level_distribution": {
    "Beginner": 8,
    "Intermediate": 5,
    "Advanced": 2
  }
}

Database Schema
Table: words

เก็บคำศัพท์ทั้งหมดในระบบ

Column	Type	Constraints	Description
id	INT	PRIMARY KEY, AUTO_INCREMENT	รหัสคำศัพท์
word	VARCHAR(100)	UNIQUE, NOT NULL	คำศัพท์ภาษาอังกฤษ
definition	TEXT		ความหมาย/คำจำกัดความ
difficulty_level	ENUM('Beginner','Intermediate','Advanced')		ระดับความยากของคำศัพท์
created_at	TIMESTAMP	DEFAULT CURRENT_TIMESTAMP	วันที่เพิ่มคำศัพท์
Table: practice_sessions

เก็บประวัติการฝึกของผู้ใช้

Column	Type	Constraints	Description
id	INT	PRIMARY KEY, AUTO_INCREMENT	รหัสการฝึก
word_id	INT	FOREIGN KEY → words(id)	คำศัพท์ที่ฝึก
user_sentence	TEXT	NOT NULL	ประโยคที่ผู้ใช้แต่ง
score	DECIMAL(3,1)		คะแนน (0.0 – 10.0)
feedback	TEXT		ข้อเสนอแนะ/คำแนะนำจากระบบ
corrected_sentence	TEXT		ประโยคที่ระบบแก้ไขแล้ว
practiced_at	TIMESTAMP	DEFAULT CURRENT_TIMESTAMP	วันเวลาที่ฝึก
ER Diagram (เชิงแนวคิด)

Development Guide
จัดการ Docker Containers

ดูสถานะ containers:

docker ps


Restart services:

# Restart ทั้งหมด
docker-compose restart

# Restart เฉพาะ FastAPI
docker-compose restart vocabapi

# Restart เฉพาะ MySQL
docker-compose restart mysql


ดู logs:

# Logs ทั้งหมด
docker-compose logs -f

# Logs เฉพาะ service
docker-compose logs -f vocabapi
docker-compose logs -f mysql


หยุด containers:

docker-compose down


ลบข้อมูลและเริ่มใหม่ (ลบ volumes ด้วย – ข้อมูลใน DB จะหายหมด):

docker-compose down -v
docker-compose up -d

การจัดการ Database ผ่าน MySQL CLI

เข้าใช้งาน MySQL ใน container:

docker exec -it vocab_mysql mysql -u vocabuser -pvocabpass123 vocabulary_db


ตัวอย่างคำสั่ง:

-- เพิ่มคำศัพท์ใหม่
INSERT INTO words (word, definition, difficulty_level) VALUES
('courage', 'The ability to do something frightening', 'Intermediate'),
('serendipity', 'Finding something good without looking for it', 'Advanced');

-- ดูคำศัพท์ทั้งหมด
SELECT * FROM words;

-- ดูประวัติการฝึก 10 รายการล่าสุด
SELECT * FROM practice_sessions
ORDER BY practiced_at DESC
LIMIT 10;

-- ดูสถิติตามระดับความยาก
SELECT
  difficulty_level,
  COUNT(*) AS total_practices,
  AVG(score) AS avg_score
FROM practice_sessions ps
JOIN words w ON ps.word_id = w.id
GROUP BY difficulty_level;


Export ข้อมูล:

docker exec vocab_mysql mysqldump -u vocabuser -pvocabpass123 vocabulary_db > backup.sql


Import ข้อมูล:

docker exec -i vocab_mysql mysql -u vocabuser -pvocabpass123 vocabulary_db < backup.sql

แนวทางพัฒนาต่อ (ไอเดียสำหรับ Term Project)
1. เชื่อมต่อ AI จริง (เช่น n8n + OpenAI)

ตอนนี้ระบบอาจใช้ฟังก์ชัน mock (ให้คะแนน/feedback แบบสุ่มหรือ rule-based)
สามารถเปลี่ยนเป็นเรียก AI จริงได้ เช่น:

สร้าง n8n workflow ที่เรียก OpenAI API

ปรับโค้ดใน API ให้ POST ไปที่ webhook ของ n8n

รับ JSON response กลับมาแล้ว map ใส่ score, feedback, corrected_sentence

2. Gamification

ระบบ Streak (ฝึกต่อเนื่องรายวัน)

ระบบ Achievements (เช่น “ฝึกครบ 50 คำ” , “ได้คะแนนเต็ม 10/10”)

Leaderboard ตามคะแนนเฉลี่ยหรือจำนวนครั้งที่ฝึก

3. Advanced Features

รูปภาพประกอบคำศัพท์ (เชื่อม Unsplash API)

Export progress ของผู้ใช้เป็น PDF report

Multi-user support (แยกข้อมูลตาม user_id)

Learning Resources
Official Documentation

FastAPI – https://fastapi.tiangolo.com

SQLAlchemy 2.0 – https://docs.sqlalchemy.org

Docker Compose – https://docs.docker.com/compose/

(ตัวอย่าง Frontend) Next.js App Router – https://nextjs.org

Made with ❤️ and ☕️ for learners


---

ถ้าอยากให้ผม “ปรับสไตล์ให้เป็นภาษาอังกฤษล้วน” หรือ “โฟกัสสำหรับอาจารย์/ผู้ตรวจงาน” บอกได้เลย เดี๋ยวผมทำ README อีกเวอร์ชันให้ 👍
::contentReference[oaicite:0]{index=0}
