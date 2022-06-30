from django import forms
from  .models import Inspection_Checklist
        
        
class Inspection_ChecklistForm(forms.ModelForm):
    class Meta:
        model = Inspection_Checklist
        fields = ['checklist_id','checklist_title','status', 'inspection_type','delete_flag']
        
