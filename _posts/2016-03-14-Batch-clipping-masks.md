---
layout: post
title: "Batch remove clipping masks from illustrator file"
date: 2016-03-14
---


{{page.title}}
I often find myself editing figures from other sources in Illustrator. Usually, importing third party files into Illustrator creates hundreds of &quot;clipping masks&quot; that need to be removed in order to edit the file. This used to take me a lot of &quot;right click - remove clipping mask&quot; steps. Anyway, I recently came across this really cool piece of code (<a target="_blank" href="https://forums.adobe.com/thread/287643?start=0&amp;tstart=0">source</a>).
<div>
<pre style="font-family: Andale Mono, Lucida Console, Monaco, fixed, monospace; color: #000000; background-color: #eee;font-size: 12px;border: 1px dashed #999999;line-height: 14px;padding: 5px; overflow: auto; width: 100%"><code> #target Illustrator  
 // script.name = RemoveClippingMasks.jsx 
 // script.description = deletes all PageItems being used as clipping masks.  
 // script.parent = Kenneth Webb // 01/07/2013  
 // script.elegant = true?  
 var docRef = app.activeDocument;  
 var clippingCount = 0  
 clipScan()  
 //loops through all pageItems, removing those that are clipping masks  
 function clipScan () {  
   for (i=docRef.pageItems.length-1;i&gt;=0;i--) {   
     if (docRef.pageItems[i].clipping == true){  
       docRef.pageItems[i].remove();  
       clippingCount++;  
     }  
   }  
 };  
 alert (&quot;All &quot;+clippingCount+&quot; Clipping Masks Removed&quot;) 
</code></pre>
<p>Just copy the above code, paste into your favorite text editor, and save using the extension &quot;.jsx&quot;. In illustrator, open the file you want to edit, click on File &#8594; Scripts &#8594; Other Script, and sit back. Depending on how many clipping masks you have this may take a while, so be patient!</p>


</div>