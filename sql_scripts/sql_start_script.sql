BEGIN;

CREATE TABLE IF NOT EXISTS public."Chat member"
(
    chat_member_id BIGINT UNIQUE NOT NULL,
    chat_type character varying(15) NOT NULL,
    time_registration timestamp with time zone NOT NULL,
    CONSTRAINT "chat_member_id_PK" PRIMARY KEY (chat_member_id)
);

CREATE TABLE IF NOT EXISTS public."Lesson"
(
    lesson_id BIGINT GENERATED ALWAYS AS IDENTITY,
    chat_member_id BIGINT NOT NULL,
    lesson_remind character varying(3) NOT NULL,
    lesson_week_type integer NOT NULL,
    lesson_day character varying(20) NOT NULL,
    lesson_time TIME WITH TIME ZONE NOT NULL,
    lesson_description character varying(200) NOT NULL,
    lesson_link character varying(500) NOT NULL,
    CONSTRAINT "lesson_id_PK" PRIMARY KEY (lesson_id),
        
    CONSTRAINT "chat_member_id_FK" FOREIGN KEY (chat_member_id)
    REFERENCES public."Chat member" (chat_member_id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID
);

END;