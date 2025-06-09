# 🐟 Biological NER Dataset – Fish Species

This folder contains the dataset used to train our **Named Entity Recognition (NER)** model tailored to biological data about fish species. The data was **collected and cleaned manually**, and annotated automatically using the **DeepSeek R1 API**.

---

## 📥 Data Collection

We collected biological texts for **2,895 fish species** to create a high-quality corpus in the context of the [Add-my-Pet (AmP)](https://www.bio.vu.nl/thb/deb/deblab/add_my_pet/index.html) portal. The data sources include:

### 1. Wikipedia  
- Scraped the **definition** and **description** sections of pages related to species in two main taxonomic classes:
  - **Chondrichthyes** (cartilaginous fishes)
  - **Actinopterygii** (ray-finned fishes)

### 2. FishBase (via AmP references)  
- Extracted reference links from AmP species pages
- Parsed valid links pointing to [FishBase](https://www.fishbase.se/) and extracted the associated textual content

✅ Final dataset:
- **2,886 Wikipedia entries**
- **1,914 FishBase entries**
- ➕ **Total: 5,905 samples (~1.3 million tokens)**

---

## 🧠 Annotation Process

The dataset was annotated using the **DeepSeek R1 API**, guided by a custom prompt template to extract **11 fine-grained biological entities**, all relevant to fish physiology and taxonomy.

### 📌 Annotated Entities:

| Entity | Description                         |
|--------|-------------------------------------|
| `Specie` | Name of the fish species           |
| `Family` | Taxonomic family of the species    |
| `ah`     | Age at hatching                    |
| `ab`     | Age at birth                       |
| `am`     | Age at death (life span)           |
| `Lb`     | Length at birth                    |
| `Lp`     | Length at puberty                  |
| `Li`     | Length at ultimate state (female)  |
| `Wwb`    | Wet weight at birth                |
| `Wwp`    | Wet weight at puberty              |
| `Wwi`    | Wet weight at ultimate state       |

> 🧪 The output was converted into **BIO format** for compatibility with standard NER training pipelines.

---