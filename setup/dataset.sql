-- =============================================================================
-- SnowPro Gen AI Exam Study Dataset
-- =============================================================================
-- PURPOSE : Single source of truth for all notebook exercises.
--           Run this script ONCE before opening any domain notebook.
-- TABLES  : GENAI_STUDY.PUBLIC.SUPPORT_TICKETS  (text / unstructured / PII)
--           GENAI_STUDY.PUBLIC.PRODUCTS          (structured / vector / analyst)
-- STAGE   : GENAI_STUDY.PUBLIC.DOCS_STAGE       (document parsing exercises)
-- =============================================================================

-- ------------------------------------------------------------
-- 0.  Database & Schema
-- ------------------------------------------------------------
CREATE DATABASE IF NOT EXISTS GENAI_STUDY;
USE DATABASE GENAI_STUDY;
CREATE SCHEMA IF NOT EXISTS PUBLIC;
USE SCHEMA PUBLIC;

-- ------------------------------------------------------------
-- 1.  SUPPORT_TICKETS
--     Drives: AI_CLASSIFY, AI_SENTIMENT, AI_SUMMARIZE,
--             AI_TRANSLATE, AI_EXTRACT, AI_FILTER, AI_AGG,
--             AI_EMBED, AI_REDACT, AI_COMPLETE, VECTOR funcs,
--             Streams, Tasks (Domain 4 pipelines)
-- ------------------------------------------------------------
CREATE OR REPLACE TABLE SUPPORT_TICKETS (
    ticket_id        NUMBER         PRIMARY KEY,
    created_at       TIMESTAMP_NTZ  DEFAULT CURRENT_TIMESTAMP(),
    resolved_at      TIMESTAMP_NTZ,
    customer_name    VARCHAR(100),           -- PII  → AI_REDACT
    email            VARCHAR(150),           -- PII  → AI_REDACT
    phone            VARCHAR(20),            -- PII  → AI_REDACT
    product_id       NUMBER,
    language         VARCHAR(10),            -- en / es / fr / de / ja
    category         VARCHAR(50),            -- billing / technical / shipping
    status           VARCHAR(20),            -- open / in_progress / resolved
    priority         VARCHAR(10),            -- low / medium / high / critical
    satisfaction_score NUMBER(3,1),          -- 1.0 – 5.0  → Cortex Analyst
    ticket_text      VARCHAR(4000),          -- rich text  → NLP functions
    resolution_notes VARCHAR(2000),
    embedding        VECTOR(FLOAT, 768)      -- populated by AI_EMBED exercise
);

INSERT INTO SUPPORT_TICKETS
    (ticket_id, created_at, resolved_at, customer_name, email, phone,
     product_id, language, category, status, priority, satisfaction_score, ticket_text, resolution_notes)
VALUES
-- English – billing
(1001, '2024-01-05 09:12:00', '2024-01-06 14:00:00',
 'Alice Johnson', 'alice.j@example.com', '+1-555-0101',
 201, 'en', 'billing', 'resolved', 'high', 4.5,
 'I was charged twice for my January subscription. My credit card statement shows two identical charges of $49.99 on Jan 3rd. Please refund the duplicate immediately. Order ID ORD-9821.',
 'Duplicate charge confirmed and refunded within 24 hours.'),

-- English – technical
(1002, '2024-01-07 11:30:00', NULL,
 'Bob Martinez', 'bob.m@example.com', '+1-555-0202',
 202, 'en', 'technical', 'open', 'critical', NULL,
 'The mobile app keeps crashing every time I try to upload a photo. Error code: APP-501. This happens on both iPhone 15 and my old iPhone 12. I need this fixed urgently as I rely on the app for my business.',
 NULL),

-- Spanish – shipping
(1003, '2024-01-08 08:45:00', '2024-01-10 16:30:00',
 'Carlos Ruiz', 'carlos.r@example.com', '+34-600-123456',
 203, 'es', 'shipping', 'resolved', 'medium', 3.0,
 'Mi pedido número PED-4421 fue marcado como entregado pero nunca llegó. Vivo en la dirección registrada y estuve en casa todo el día. Necesito una investigación o reenvío del paquete.',
 'Paquete reenviado con número de seguimiento TRK-8832.'),

-- French – technical
(1004, '2024-01-09 14:00:00', NULL,
 'Marie Dupont', 'marie.d@example.com', '+33-6-12345678',
 202, 'fr', 'technical', 'in_progress', 'high', NULL,
 'Je ne peux pas me connecter à mon compte depuis hier soir. Le message d erreur indique "identifiants invalides" mais je suis certain de mon mot de passe. Pouvez-vous réinitialiser mon compte?',
 NULL),

-- English – billing
(1005, '2024-01-10 10:00:00', '2024-01-11 09:00:00',
 'Diana Chen', 'diana.c@example.com', '+1-555-0303',
 204, 'en', 'billing', 'resolved', 'low', 5.0,
 'I upgraded to the Pro plan last week but my account still shows the Basic plan features. I was charged $99/month but cannot access advanced analytics or the API. Invoice INV-20240110.',
 'Account upgraded in backend system. Features now available.'),

-- German – shipping
(1006, '2024-01-11 13:15:00', '2024-01-14 11:00:00',
 'Hans Müller', 'hans.m@example.com', '+49-170-1234567',
 205, 'de', 'shipping', 'resolved', 'medium', 4.0,
 'Meine Bestellung B-9933 ist seit 10 Tagen im Versandzentrum Frankfurt blockiert. Laut Tracking-System gibt es ein Zollproblem, obwohl ich ein inländischer Kunde bin. Bitte klären Sie dies umgehend.',
 'Versandproblem behoben. Paket wurde am 14.01 zugestellt.'),

-- English – technical (very negative sentiment)
(1007, '2024-01-12 16:45:00', NULL,
 'Eve Williams', 'eve.w@example.com', '+1-555-0404',
 202, 'en', 'technical', 'open', 'critical', NULL,
 'This is absolutely unacceptable. For the third time this month the entire platform is down during business hours. We are losing thousands of dollars every hour. I demand a full SLA credit and an explanation from your engineering team. Incident INC-7701.',
 NULL),

-- Japanese – billing
(1008, '2024-01-13 09:00:00', '2024-01-15 12:00:00',
 'Yuki Tanaka', 'yuki.t@example.com', '+81-90-1234-5678',
 201, 'ja', 'billing', 'resolved', 'medium', 4.2,
 '先月の請求額が通常より高くなっています。契約プランはスタンダードプランのはずなのに、プレミアムプランの料金が請求されています。請求書番号はINV-20240113です。確認をお願いします。',
 'Billing corrected. Refund processed for overage amount.'),

-- English – shipping (positive)
(1009, '2024-01-14 11:30:00', '2024-01-14 14:00:00',
 'Frank Lee', 'frank.l@example.com', '+1-555-0505',
 205, 'en', 'shipping', 'resolved', 'low', 5.0,
 'Just wanted to say your team was amazing! My package arrived two days early and the packaging was perfect. The customer service rep Sarah was incredibly helpful when I had a question about delivery times.',
 'Positive feedback shared with the shipping team.'),

-- English – technical (security concern)
(1010, '2024-01-15 08:00:00', NULL,
 'Grace Kim', 'grace.k@example.com', '+1-555-0606',
 202, 'en', 'technical', 'in_progress', 'critical', NULL,
 'I received an email saying my account was accessed from an unknown location (IP: 192.168.x.x, location: Eastern Europe). I did not authorize this login. Please lock my account immediately, reset all tokens, and investigate this potential security breach. SSN: 123-45-6789.',
 NULL),

-- English – billing (medium sentiment)
(1011, '2024-01-16 15:00:00', '2024-01-17 10:00:00',
 'Henry Brown', 'henry.b@example.com', '+1-555-0707',
 204, 'en', 'billing', 'resolved', 'medium', 3.5,
 'I cancelled my subscription on December 28th but was still charged for January. I have the cancellation confirmation email (Case ID: CXL-4456). Please process the refund and confirm my account is fully cancelled.',
 'Refund issued. Account cancellation confirmed.'),

-- English – technical (medium complexity)
(1012, '2024-01-17 10:30:00', NULL,
 'Iris Patel', 'iris.p@example.com', '+44-7911-123456',
 203, 'en', 'technical', 'open', 'high', NULL,
 'The data export feature is producing corrupted CSV files. When I open the downloaded file, all text fields containing commas are malformed. This affects our nightly data pipeline to our data warehouse. The bug appears to have been introduced in the v3.2.1 release.',
 NULL);


-- ------------------------------------------------------------
-- 2.  PRODUCTS
--     Drives: Cortex Analyst (Text-to-SQL), AI_EMBED,
--             AI_SIMILARITY, VECTOR_COSINE_SIMILARITY,
--             AI_SUMMARIZE_AGG, AI_COMPLETE
-- ------------------------------------------------------------
CREATE OR REPLACE TABLE PRODUCTS (
    product_id       NUMBER         PRIMARY KEY,
    product_name     VARCHAR(100),
    category         VARCHAR(50),
    sub_category     VARCHAR(50),
    description      VARCHAR(2000),           -- embeddings + similarity
    price            NUMBER(10,2),
    monthly_revenue  NUMBER(12,2),
    units_sold       NUMBER,
    region           VARCHAR(50),
    launch_date      DATE,
    rating           NUMBER(3,1),             -- 1.0 – 5.0
    review_summary   VARCHAR(1000),           -- AI_SUMMARIZE_AGG target
    is_active        BOOLEAN DEFAULT TRUE,
    embedding        VECTOR(FLOAT, 768)       -- populated by AI_EMBED exercise
);

INSERT INTO PRODUCTS
    (product_id, product_name, category, sub_category, description, price,
     monthly_revenue, units_sold, region, launch_date, rating, review_summary)
VALUES
(201, 'CloudSync Basic', 'Software', 'Subscription',
 'Entry-level cloud storage and file synchronization service. Includes 100GB storage, cross-device sync, and basic version history. Ideal for individual users and freelancers who need reliable file backup.',
 49.99, 125000.00, 2500, 'North America', '2022-03-15', 4.1,
 'Users love the ease of setup and reliability. Common complaints include limited storage and lack of advanced sharing features.'),

(202, 'CloudSync Pro', 'Software', 'Subscription',
 'Professional-grade cloud platform with 2TB storage, advanced collaboration tools, real-time co-editing, REST API access, and enterprise-grade security. Designed for teams of up to 50 users.',
 99.00, 495000.00, 5000, 'North America', '2022-06-01', 3.9,
 'Teams appreciate the API and collaboration features. Stability issues during peak hours and mobile app crashes reported frequently.'),

(203, 'ShipTrack Lite', 'Logistics', 'Tracking',
 'Lightweight shipment tracking widget that integrates with major carriers including FedEx, UPS, DHL, and USPS. Provides real-time status updates, delivery notifications, and basic analytics dashboard.',
 19.99, 39800.00, 1990, 'Europe', '2023-01-20', 4.3,
 'Praised for its simplicity and carrier coverage. Some users report delays in status updates for international shipments.'),

(204, 'Analytics Suite', 'Analytics', 'Business Intelligence',
 'Comprehensive business intelligence platform with drag-and-drop dashboards, 200+ data connectors, predictive analytics powered by ML models, scheduled reporting, and role-based access control.',
 299.00, 897000.00, 3000, 'Global', '2021-11-10', 4.6,
 'Highly rated for depth of features and connector library. Learning curve is steep for non-technical users. Excellent enterprise support.'),

(205, 'PackagePlus', 'Logistics', 'Fulfillment',
 'End-to-end order fulfillment solution with automated picking, packing recommendations, multi-warehouse inventory management, and one-click shipping label generation for e-commerce businesses.',
 149.00, 596000.00, 4000, 'North America', '2023-05-05', 4.7,
 'Widely regarded as best-in-class for e-commerce fulfillment. Users highlight time savings and inventory accuracy improvements.'),

(206, 'SecureVault', 'Security', 'Compliance',
 'Enterprise data vault solution providing encryption at rest and in transit, automated compliance reporting for GDPR, HIPAA and SOC 2, key management, and audit trail logging.',
 499.00, 1497000.00, 3000, 'Global', '2020-09-01', 4.8,
 'Security teams and compliance officers give this the highest marks. Integration with existing IAM systems praised. Pricing considered high by SMBs.'),

(207, 'DataStream AI', 'Analytics', 'AI/ML',
 'Real-time data streaming platform with built-in AI/ML model inference, feature engineering pipelines, and Snowflake-native integration. Handles up to 10M events per second with sub-100ms latency.',
 799.00, 1598000.00, 2000, 'Global', '2024-02-14', 4.5,
 'Data engineers love the Snowflake integration and low latency. Initial setup complexity noted. Documentation improvements requested.'),

(208, 'MobileFirst SDK', 'Developer Tools', 'SDK',
 'Cross-platform mobile SDK supporting iOS and Android. Includes authentication modules, push notification services, crash reporting, analytics hooks, and offline data sync capabilities.',
 39.99, 79980.00, 2000, 'Asia Pacific', '2023-08-01', 3.7,
 'Developers appreciate the comprehensive feature set. Crash reporting module has known issues on older Android versions. iOS experience rated higher than Android.');


-- ------------------------------------------------------------
-- 3.  DOCS_STAGE  (for Domain 4 – document parsing exercises)
--
--     Server-side encryption is set explicitly. A FILE object cannot be
--     built over a fully client-side-encrypted stage, so the default here
--     matters: get it wrong and TO_FILE() fails later with an error that
--     does not mention encryption.
-- ------------------------------------------------------------
CREATE STAGE IF NOT EXISTS DOCS_STAGE
    ENCRYPTION = (TYPE = 'SNOWFLAKE_SSE')
    DIRECTORY = (ENABLE = TRUE)
    COMMENT = 'Sample documents for AI_PARSE_DOCUMENT and AI_EXTRACT exercises';

-- Upload the sample documents from the repo's sample_docs/ folder.
-- From SnowSQL or the Snowflake CLI, run these from the repo root:
--
--   PUT file://sample_docs/invoice_KF-2041.pdf                 @GENAI_STUDY.PUBLIC.DOCS_STAGE AUTO_COMPRESS=FALSE;
--   PUT file://sample_docs/invoice_AV-8817.pdf                 @GENAI_STUDY.PUBLIC.DOCS_STAGE AUTO_COMPRESS=FALSE;
--   PUT file://sample_docs/invoice_TS-5530.pdf                 @GENAI_STUDY.PUBLIC.DOCS_STAGE AUTO_COMPRESS=FALSE;
--   PUT file://sample_docs/contract_msa_harbourview.pdf        @GENAI_STUDY.PUBLIC.DOCS_STAGE AUTO_COMPRESS=FALSE;
--   PUT file://sample_docs/financial_statement_mgc_q3_2026.pdf @GENAI_STUDY.PUBLIC.DOCS_STAGE AUTO_COMPRESS=FALSE;
--   PUT file://sample_docs/support_tickets.txt                 @GENAI_STUDY.PUBLIC.DOCS_STAGE AUTO_COMPRESS=FALSE;
--
-- AUTO_COMPRESS=FALSE matters: PUT gzips files by default, and a .pdf.gz
-- on the stage is not a PDF any more. AI_PARSE_DOCUMENT will reject it.
--
-- In Snowsight you can instead use Data > Databases > GENAI_STUDY > PUBLIC >
-- Stages > DOCS_STAGE > + Files, which does not compress.
--
-- Then refresh the directory table so DIRECTORY() sees the new files:
--   ALTER STAGE DOCS_STAGE REFRESH;
--   SELECT RELATIVE_PATH, SIZE, LAST_MODIFIED FROM DIRECTORY(@DOCS_STAGE);

-- ------------------------------------------------------------
-- 4.  STREAM on SUPPORT_TICKETS (for Domain 4 pipeline exercises)
-- ------------------------------------------------------------
CREATE OR REPLACE STREAM SUPPORT_TICKETS_STREAM
    ON TABLE SUPPORT_TICKETS
    COMMENT = 'CDC stream for pipeline automation exercises in Domain 2.4 and 4.3';

-- ------------------------------------------------------------
-- 5.  Quick sanity check
-- ------------------------------------------------------------
SELECT 'SUPPORT_TICKETS' AS tbl, COUNT(*) AS row_s FROM SUPPORT_TICKETS
UNION ALL
SELECT 'PRODUCTS',               COUNT(*)          FROM PRODUCTS;



