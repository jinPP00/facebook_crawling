def style_css():
  style_content = """
<style>
#grid {
grid-template-columns: 200px 1fr;
max-width: 800px;
height: 200px;
box-sizing: border-box;
}
.vlp-link-text-container {
padding: 33px 46px 0px 39px;
white-space: nowrap;
overflow: hidden;
text-overflow: ellipsis;
}

.vlp-link-title {
font-size: 22px;
margin: 0px 0px 10px;
white-space: nowrap;
overflow: hidden;
text-overflow: ellipsis;
}

.vlp-link-summary {
white-space: normal;
text-align: left;
line-height: 1.4;
max-height: 2.8em;
overflow: hidden;
margin: 0px 0px 25px;
}

@media(max-width:600px){
#grid {
grid-template-columns: 120px 1fr;	
height: 120px;
box-sizing: border-box;
}
.vlp-link-text-container {
padding: 24px 12px 0px 18px;
}
.vlp-link-title{
margin: 0px 0px 10px 0px;
white-space: nowrap;
font-size: 17px;
}
.vlp-link-summary {
display:none;
}
.vlp-link-image{
max-width:120px;	max-height:120px;
}
}
</style>
"""
  return style_content
if __name__ == "__main__":
  print(style_css())



# <table style="border: none; width: 100%;" data-ke-align="alignLeft">
#   <tbody>
#     <tr style="border: none;">
#       <td style="background-color: #17c5b3; border-radius: 20px; color: white; padding: 10px; text-align: center;">
#         <span><b>특고 프리랜서 6차 재난지원금 신규신청 대상은?</b></span></td>
#     </tr>
#     <tr style="border: none;">
#       <td style="background-color: #f0f0f0; border-radius: 20px; color: black; padding: 10px; text-align: center;">
#         <span><b>특고 프리랜서 6차 재난지원금 신규신청 대상은?</b></span></td>
#     </tr>
#   </tbody>
# </table>

