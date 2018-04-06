--
-- Create model Class
--
CREATE TABLE "students_class" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "class_code" varchar(20) NOT NULL UNIQUE, "class_name" varchar(20) NOT NULL, "section" varchar(5) NOT NULL, "class_Teacher" varchar(20) NOT NULL);
--
-- Create model Parents
--
CREATE TABLE "students_parents" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "name" varchar(20) NOT NULL, "contact" varchar(20) NOT NULL, "gender" varchar(1) NULL, "relation" varchar(50) NOT NULL);
--
-- Create model Student
--
CREATE TABLE "students_student" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "Roll_Num" varchar(20) NOT NULL UNIQUE, "Name" varchar(150) NOT NULL, "Address" varchar(200) NOT NULL, "parent_code" varchar(20) NOT NULL, "class_code_id" integer NOT NULL REFERENCES "students_class" ("id") DEFERRABLE INITIALLY DEFERRED);
--
-- Create model SubjectEnroll
--
CREATE TABLE "students_subjectenroll" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "Roll_Num_id" integer NOT NULL REFERENCES "students_student" ("id") DEFERRABLE INITIALLY DEFERRED);
--
-- Create model Subjects
--
CREATE TABLE "students_subjects" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "subject_code" varchar(20) NOT NULL UNIQUE, "subject_name" varchar(100) NOT NULL, "details" varchar(500) NOT NULL, "class_code_id" integer NOT NULL REFERENCES "students_class" ("id") DEFERRABLE INITIALLY DEFERRED);
--
-- Add field subject_code to subjectenroll
--
ALTER TABLE "students_subjectenroll" RENAME TO "students_subjectenroll__old";
CREATE TABLE "students_subjectenroll" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "Roll_Num_id" integer NOT NULL REFERENCES "students_student" ("id") DEFERRABLE INITIALLY DEFERRED, "subject_code_id" integer NOT NULL REFERENCES "students_subjects" ("id") DEFERRABLE INITIALLY DEFERRED);
INSERT INTO "students_subjectenroll" ("id", "Roll_Num_id", "subject_code_id") SELECT "id", "Roll_Num_id", NULL FROM "students_subjectenroll__old";
DROP TABLE "students_subjectenroll__old";
CREATE INDEX "students_student_class_code_id_25d0bd4d" ON "students_student" ("class_code_id");
CREATE INDEX "students_subjects_class_code_id_2bd016a7" ON "students_subjects" ("class_code_id");
CREATE INDEX "students_subjectenroll_Roll_Num_id_a806f74e" ON "students_subjectenroll" ("Roll_Num_id");
CREATE INDEX "students_subjectenroll_subject_code_id_2d3a76b7" ON "students_subjectenroll" ("subject_code_id");
--
-- Add field Roll_Num to parents
--
ALTER TABLE "students_parents" RENAME TO "students_parents__old";
CREATE TABLE "students_parents" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "name" varchar(20) NOT NULL, "contact" varchar(20) NOT NULL, "gender" varchar(1) NULL, "relation" varchar(50) NOT NULL, "Roll_Num_id" integer NOT NULL REFERENCES "students_student" ("id") DEFERRABLE INITIALLY DEFERRED);
INSERT INTO "students_parents" ("id", "name", "contact", "gender", "relation", "Roll_Num_id") SELECT "id", "name", "contact", "gender", "relation", NULL FROM "students_parents__old";
DROP TABLE "students_parents__old";
CREATE INDEX "students_parents_Roll_Num_id_0dcfd56c" ON "students_parents" ("Roll_Num_id");
COMMIT;