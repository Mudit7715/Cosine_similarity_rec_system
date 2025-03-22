import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import streamlit as st

roles = [
    "Data Scientist", "ML Engineer", "Data Analyst", "Data Engineer",
    "AI Researcher", "Business Analyst", "NLP Engineer"
]

skills = [
    ["Python", "Statistics", "Machine Learning", "Data Visualization"],
    ["Python", "Machine Learning", "Deployment", "Algorithms"],
    ["SQL", "Python", "Data Visualization", "Excel"],
    ["Python", "SQL", "ETL", "Cloud Computing"],
    ["Python", "Deep Learning", "Machine Learning", "Algorithms"],
    ["Excel", "SQL", "Data Visualization", "Business Intelligence"],
    ["Python", "NLP", "Machine Learning", "Deep Learning"]
]

skills_text = [' '.join(skill_list) for skill_list in skills]

vectorizer = CountVectorizer()
skill_vectors = vectorizer.fit_transform(skills_text)

similarity_matrix = cosine_similarity(skill_vectors)

def get_recommendations(role_name, similarity_matrix=similarity_matrix, roles=roles, skills=skills):
    role_index = roles.index(role_name)
    similarity_scores = list(enumerate(similarity_matrix[role_index]))
    similarity_scores = sorted([(i, score) for i, score in similarity_scores if i != role_index], 
                              key=lambda x: x[1], reverse=True)
    top_roles = similarity_scores[:3]
    recommendations = []
    for idx, score in top_roles:
        shared_skills = set(skills[role_index]) & set(skills[idx])
        recommendations.append({
            'role': roles[idx],
            'similarity': round(score, 2),
            'skills': skills[idx],
            'shared_skills': list(shared_skills)
        })
    
    return recommendations

def main():
    st.title("Job Role Recommendation System")
    st.write("Find similar job roles based on shared skills")
    
    # Display job roles table
    df = pd.DataFrame({
        'Role': roles,
        'Skills': [', '.join(s) for s in skills]
    })
    st.table(df)
    
    selected_role = st.selectbox("Select a job role:", roles)
    
    if st.button("Find Similar Roles"):
        recommendations = get_recommendations(selected_role)
        
        st.subheader(f"Top 3 roles similar to {selected_role}:")
        for i, rec in enumerate(recommendations, 1):
            st.write(f"{i}. {rec['role']} (Similarity: {rec['similarity']})")
            st.write(f"   Skills: {', '.join(rec['skills'])}")
            st.write(f"   Shared skills: {', '.join(rec['shared_skills'])}")

if __name__ == "__main__":
    main()
