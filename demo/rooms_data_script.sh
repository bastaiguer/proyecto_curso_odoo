#!/bin/bash/
i=0;

echo '<odoo><data>'
arrayString=("Habitación discreta" "Habitación de lujo" "Habitación familiar")
while [ $i -lt 400 ] ; do
	camas=$((( RANDOM % 3 ) + 1))
	price=$((( RANDOM % 120 ) + 25))
        hotel=$((( RANDOM % 4 ) + 0))
        num_photo=$((( RANDOM % 3 ) + 0))
        num_photo2=$((( RANDOM % 3 ) + 0))
while [ $num_photo -eq $num_photo2 ] ; do
        num_photo2=$((( RANDOM % 3 ) + 0))
done
	photo="ref('hoteltrivago.photo_r"$num_photo"')"
	photo2="ref('hoteltrivago.photo_r"$num_photo2"')"

if [ $price -gt 110 ] ; then
	n=1
else
if [ $camas -gt 2 ] ; then
	n=2
else
	n=0
fi
fi
	echo '
		<record id="room'$i'" model="hoteltrivago.rooms">
			<field name="name">Room '$i'</field>
			<field name="beds">'$camas'</field>
			<field name="price">'$price'</field>
			<field name="description">'${arrayString[$n]}'</field> 
			<field name="photos" eval="[(6,0,['$photo', '$photo2'])]"/>
			<field name="hotels" ref="hoteltrivago.hotel'$hotel'"/>
		</record>
'

i=$(($i+1));
done
echo '</data></odoo>'
