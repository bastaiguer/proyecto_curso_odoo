#!/bin/bash/
i=0;
echo '
<odoo>
  <data>'

while [ $i -lt 4 ] ; do
	city=$((( RANDOM % 2 ) + 0))
	ns=$((( RANDOM % 5 ) + 1))
	servicen=$((( RANDOM % 5) + 0))
	photo1="'hoteltrivago.photo_h0'"
	photo2="'hoteltrivago.photo_h1'"
	service="'hoteltrivago.service"$servicen"'"
	servicen2=$servicen
	while [ $servicen -eq $servicen2 ] ; do
	servicen2=$((( RANDOM % 5) + 0))
	service2="'hoteltrivago.service"$servicen2"'"
	done
	echo '
    <record id="hotel'$i'" model="hoteltrivago.hotels">
      <field name="name">Hotel '$i'</field>
      <field name="stars">'$ns'</field>
      <field name="description">Description'$ns'</field>
      <field name="city" ref="hoteltrivago.city'$city'"/>
      <field name="gallery" eval="[(6,0,[ref('$photo1'), ref('$photo2')])]"/>
      <field name="services" eval="[(6,0,[ref('$service'),ref('$service2')])]" />
    </record>
'
i=$(($i+1))
done
echo '
  </data>
</odoo>'
