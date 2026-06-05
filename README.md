# AI Career Navigator - Data Science

## Overview

Repository ini berisi seluruh proses Data Science untuk proyek **AI Career Navigator**, mulai dari Exploratory Data Analysis (EDA), preprocessing data, hingga pengembangan sistem Skill Gap Recommendation berbasis data lowongan pekerjaan.

## Dataset

Dataset yang digunakan berasal dari lowongan pekerjaan teknologi yang berisi:

* Company
* Job Title
* Job Type
* Experience Level
* Skills

Dataset yang tersedia:

* `cleaned_dataset_job.csv`
* `job_dataset_processed.csv`

## Project Workflow

```text
EDA
↓
Preprocessing
↓
Career Family Mapping
↓
Skill Gap Recommendation
```

## Notebooks

### 1. eda_job_dataset.ipynb

Analisis eksploratif terhadap dataset lowongan pekerjaan untuk memahami distribusi role, skill, job type, dan experience level.

### 2. preprocessing_job_dataset.ipynb

Pembersihan data, feature engineering, text preprocessing, dan transformasi data menggunakan TF-IDF.

### 3. skill_gap_recommendation.ipynb

Sistem rekomendasi skill gap berdasarkan role target dan skill yang dimiliki pengguna.

## Business Questions

1. Role teknologi apa yang paling banyak dicari industri?
2. Skill teknis apa yang paling sering muncul pada lowongan kerja?
3. Bagaimana distribusi tingkat pengalaman pada lowongan kerja?
4. Mengapa job title normalization diperlukan sebelum modeling?
5. Skill apa yang perlu dipelajari pengguna untuk mencapai role tertentu?

## Career Family

Role yang digunakan dalam sistem:

* Data Analyst
* Data Scientist
* Data Engineer
* Machine Learning Engineer
* Software Engineer
* Business Analyst
* QA Engineer

## Outputs

* Exploratory Data Analysis (EDA)
* Processed Dataset
* TF-IDF Feature Representation
* Career Family Mapping
* Job Skill Mapping
* Skill Gap Recommendation

## Capstone Project

Coding Camp powered by DBS Foundation

AI Career Navigator – Career Recommendation & Skill Gap Analysis System
